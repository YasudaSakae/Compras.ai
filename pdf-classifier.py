import os
import shutil
from PyPDF2 import PdfReader
import re
import time
from datetime import datetime
from typing import Dict, List, Tuple

class Timer:
    def __init__(self):
        self.times: Dict[str, List[float]] = {}
        
    def add_time(self, operation: str, duration: float):
        if operation not in self.times:
            self.times[operation] = []
        self.times[operation].append(duration)
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        stats = {}
        for op, times in self.times.items():
            if not times:
                continue
            stats[op] = {
                'média': sum(times) / len(times),
                'min': min(times),
                'max': max(times),
                'total': sum(times)
            }
        return stats

def create_folders(base_path: str, timer: Timer):
    start = time.time()
    folders = [
        'Concorrência', 'Credenciamento', 'Dispensa', 'Inexigibilidade',
        'Leilão', 'Manifestação de Interesse', 'Pregão', 'Outros',
        'Não Lidos', 'Imagens'
    ]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    timer.add_time('criar_pastas', time.time() - start)

def extract_text_from_pdf(pdf_path: str, timer: Timer) -> Tuple[str, bool]:
    start = time.time()
    try:
        reader = PdfReader(pdf_path)
        text = ""
        words_count = 0
        
        for page in reader.pages:
            if words_count >= 100:
                break
            
            page_text = page.extract_text()
            if not page_text:
                continue
                
            words = page_text.split()
            remaining_words = 100 - words_count
            text += " ".join(words[:remaining_words]) + " "
            words_count += len(words[:remaining_words])
            
        timer.add_time('extrair_texto', time.time() - start)
        return text.lower(), True
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {str(e)}")
        timer.add_time('erro_leitura', time.time() - start)
        return "", False

def classify_pdf(text: str, timer: Timer) -> str:
    start = time.time()
    if not text:
        timer.add_time('classificar', time.time() - start)
        return "Imagens"
        
    keywords = {
        'Concorrência': ['concorrência', 'concorrencia'],
        'Credenciamento': ['credenciamento'],
        'Dispensa': ['dispensa'],
        'Inexigibilidade': ['inexigibilidade'],
        'Leilão': ['leilão', 'leilao'],
        'Manifestação de Interesse': ['manifestação de interesse', 'manifestacao de interesse'],
        'Pregão': ['pregão', 'pregao']
    }
    
    for category, terms in keywords.items():
        for term in terms:
            if term in text:
                timer.add_time('classificar', time.time() - start)
                return category
    
    timer.add_time('classificar', time.time() - start)
    return "Outros"

def move_file(source: str, dest_folder: str, filename: str, timer: Timer):
    start = time.time()
    shutil.move(source, os.path.join(dest_folder, filename))
    timer.add_time('mover_arquivo', time.time() - start)

def process_pdfs(input_path: str):
    timer = Timer()
    total_start = time.time()
    
    create_folders(input_path, timer)
    
    files_processed = 0
    for filename in os.listdir(input_path):
        if not filename.lower().endswith('.pdf'):
            continue
            
        files_processed += 1
        pdf_path = os.path.join(input_path, filename)
        
        text, success = extract_text_from_pdf(pdf_path, timer)
        
        if not success:
            category = "Não Lidos"
        else:
            category = classify_pdf(text, timer)
            
        dest_folder = os.path.join(input_path, category)
        move_file(pdf_path, dest_folder, filename, timer)
        print(f"Movido {filename} para {category}")
    
    total_time = time.time() - total_start
    timer.add_time('tempo_total', total_time)
    
    # Imprime estatísticas
    print("\nEstatísticas de tempo (em segundos):")
    stats = timer.get_stats()
    for operation, metrics in stats.items():
        print(f"\n{operation.upper()}:")
        print(f"  Média: {metrics['média']:.3f}")
        print(f"  Mínimo: {metrics['min']:.3f}")
        print(f"  Máximo: {metrics['max']:.3f}")
        print(f"  Total: {metrics['total']:.3f}")
    
    if files_processed > 0:
        print(f"\nTempo médio por arquivo: {total_time/files_processed:.3f} segundos")
        print(f"Total de arquivos processados: {files_processed}")

if __name__ == "__main__":
    input_path = input("Digite o caminho da pasta com os PDFs: ")
    process_pdfs(input_path)
