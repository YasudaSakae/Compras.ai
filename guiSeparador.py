import os
import shutil
from PyPDF2 import PdfReader
import time
from typing import Dict, List, Tuple
from unidecode import unidecode
import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
import threading
from functools import wraps

class TimeoutException(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [TimeoutException('Timed out')]
            def worker():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                return None
            if isinstance(result[0], Exception):
                raise result[0]
            return result[0]
        return wrapper
    return decorator

class Timer:
    def __init__(self):
        self.times: Dict[str, List[float]] = {}
        
    def add_time(self, operation: str, duration: float):
        if operation not in self.times:
            self.times[operation] = []
        self.times[operation].append(duration)
        
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        return {op: {
            'média': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'total': sum(times)
        } for op, times in self.times.items() if times}

class TextProcessor:
    def __init__(self):
        self.keywords = {
            'Contratação': [r'\b(contrata[çc][ãa]o|contrato)\b'],
            'Credenciamento': [r'\bcredenciamento\b'],
            'Dispensa': [r'\bdispensa\b'],
            'Inexigibilidade': [r'\binexigibilidade\b'],
            'Leilão': [r'\bleil[ãa]o\b'],
            'Manifestação de Interesse': [r'\bmanifesta[çc][ãa]o\s+de\s+interesse\b'],
            'Pregão': [r'\bpreg[ãa]o\b'],
            'Termo de Referência': [r'\b(termo\s+de\s+refer[êe]ncia|tr)\b'],
            'Estudo Técnico Preliminar': [r'\bestudo\s+t[ée]cnico\s+preliminar\b'],
            'Matriz de Gerenciamento de Riscos': [r'\bmatriz\s+de\s+gerenciamento\s+de\s+riscos\b']
        }
        
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = unidecode(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

class PDFProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Classificador de PDFs")
        self.root.geometry("800x600")
        
        # Configurar redimensionamento
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid do frame principal
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        
        # Seleção de pasta
        ttk.Label(main_frame, text="Pasta com PDFs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_path)
        folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Selecionar", command=self.select_folder).grid(row=0, column=2, pady=5)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Frame para log e scrollbar
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)
        
        # Status com scrollbar
        self.status_text = tk.Text(log_frame, wrap=tk.WORD)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Botão processar
        self.process_button = ttk.Button(main_frame, text="Processar PDFs", 
                                       command=self.start_processing)
        self.process_button.grid(row=3, column=0, columnspan=3, pady=10)
        
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        
    def update_progress(self, current, total):
        self.progress_var.set((current / total) * 100)
        self.root.update_idletasks()
        
    def start_processing(self):
        if not self.folder_path.get():
            self.log_message("Selecione uma pasta primeiro!")
            return
            
        self.process_button.configure(state='disabled')
        self.status_text.delete(1.0, tk.END)
        self.log_message("Iniciando processamento...")
        
        thread = threading.Thread(target=self.process_pdfs)
        thread.daemon = True
        thread.start()

    @timeout(10)
    def extract_text_from_pdf(self, pdf_path: str, timer: Timer) -> Tuple[str, str, bool]:
        start = time.time()
        try:
            reader = PdfReader(pdf_path)
            if not reader.pages:
                timer.add_time('erro_leitura', time.time() - start)
                return "", "", False
                
            first_page = reader.pages[0].extract_text()
            title = ' '.join(first_page.split()[:10])
            
            text_chunks = []
            total_words = 0
            
            for page in reader.pages:
                if total_words >= 150:
                    break
                
                page_text = page.extract_text()
                if not page_text:
                    continue
                
                words = page_text.split()
                chunk = words[:150-total_words]
                text_chunks.append(' '.join(chunk))
                total_words += len(chunk)
                
            timer.add_time('extrair_texto', time.time() - start)
            return title.lower(), ' '.join(text_chunks).lower(), True
        except Exception as e:
            timer.add_time('erro_leitura', time.time() - start)
            return "", "", False

    @timeout(10)
    def classify_pdf(self, title: str, content: str, processor: TextProcessor, timer: Timer) -> str:
        start = time.time()
        if not content and not title:
            timer.add_time('classificar', time.time() - start)
            return "Imagens"
        
        cleaned_title = processor.clean_text(title)
        cleaned_content = processor.clean_text(content)
        
        # Verifica primeiro no título
        for category, patterns in processor.keywords.items():
            for pattern in patterns:
                if re.search(pattern, cleaned_title):
                    timer.add_time('classificar', time.time() - start)
                    return category
        
        # Se não encontrou no título, procura no conteúdo
        content_matches = {}
        for category, patterns in processor.keywords.items():
            for pattern in patterns:
                content_matches[category] = len(re.findall(pattern, cleaned_content))
        
        best_match = max(content_matches.items(), key=lambda x: x[1])
        timer.add_time('classificar', time.time() - start)
        
        return best_match[0] if best_match[1] > 0 else "Outros"
        
    def process_pdfs(self):
        try:
            timer = Timer()
            processor = TextProcessor()
            input_path = self.folder_path.get()
            
            self.log_message("Criando pastas...")
            create_folders(input_path, timer)
            
            stats = {'processed': 0, 'moved': {}, 'errors': 0}
            pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
            total_files = len(pdf_files)
            
            if total_files == 0:
                self.log_message("Nenhum arquivo PDF encontrado na pasta!")
                return
                
            self.log_message(f"Encontrados {total_files} arquivos PDF")
            
            for filename in pdf_files:
                try:
                    pdf_path = os.path.join(input_path, filename)
                    stats['processed'] += 1
                    
                    if os.path.getsize(pdf_path) < 100:
                        self.log_message(f"Arquivo muito pequeno: {filename}")
                        category = "Não Lidos"
                    else:
                        result = self.extract_text_from_pdf(pdf_path, timer)
                        if result is None:
                            self.log_message(f"Timeout ao processar: {filename}")
                            category = "Não Lidos"
                        else:
                            title, content, success = result
                            if not success:
                                category = "Não Lidos"
                            else:
                                classification_result = self.classify_pdf(title, content, processor, timer)
                                category = "Não Lidos" if classification_result is None else classification_result
                    
                    dest_folder = os.path.join(input_path, category)
                    shutil.move(pdf_path, os.path.join(dest_folder, filename))
                    stats['moved'][category] = stats['moved'].get(category, 0) + 1
                    
                    progress_msg = f"Processado {stats['processed']}/{total_files} ({(stats['processed']/total_files*100):.1f}%): {filename} → {category}"
                    self.log_message(progress_msg)
                    self.update_progress(stats['processed'], total_files)
                    
                except Exception as e:
                    self.log_message(f"Erro ao processar {filename}: {str(e)}")
                    stats['errors'] += 1
                
            # Estatísticas finais
            self.log_message("\nEstatísticas:")
            total_moved = sum(stats['moved'].values())
            for category, count in stats['moved'].items():
                percentage = (count / total_moved) * 100 if total_moved > 0 else 0
                self.log_message(f"{category}: {count} ({percentage:.1f}%)")
            
            if stats['errors'] > 0:
                error_percentage = (stats['errors'] / stats['processed']) * 100
                self.log_message(f"\nErros: {stats['errors']} ({error_percentage:.1f}%)")
                
            self.log_message("\nProcessamento concluído!")
            
        except Exception as e:
            self.log_message(f"Erro durante o processamento: {str(e)}")
        finally:
            self.root.after(0, lambda: self.process_button.configure(state='normal'))

def create_folders(base_path: str, timer: Timer) -> None:
    start = time.time()
    folders = [
        'Contratação', 'Credenciamento', 'Dispensa', 'Inexigibilidade',
        'Leilão', 'Manifestação de Interesse', 'Pregão', 'Outros',
        'Não Lidos', 'Imagens', 'Termo de Referência', 'Estudo Técnico Preliminar',
        'Matriz de Gerenciamento de Riscos'
    ]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    timer.add_time('criar_pastas', time.time() - start)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFProcessorGUI(root)
    root.mainloop()
