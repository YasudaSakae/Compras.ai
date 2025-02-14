import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader
import os
import requests
import logging
import time
from datetime import datetime
import google.generativeai as genai

class PDFAnalyzer:
    def __init__(self):
        self.setup_logging()
        
        self.window = tk.Tk()
        self.window.title("Analisador de PDFs com Gemini")
        self.window.geometry("1200x800")
        self.window.minsize(800, 600)
        
        self.setup_ui()
        self.selected_files = []
        self.logger = logging.getLogger(__name__)

    def setup_logging(self):
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = os.path.join(log_dir, f'pdf_analyzer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.window, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=3)
        
        self.setup_config_frame()
        self.setup_files_frame()
        self.setup_process_button()
        self.setup_result_area()

    def setup_config_frame(self):
        config_frame = ttk.LabelFrame(self.main_frame, text="Configurações Gemini")
        config_frame.grid(row=0, column=0, sticky='ew', pady=5)
        config_frame.columnconfigure(1, weight=1)
        
        # API Key
        ttk.Label(config_frame, text="API Key:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.api_key_entry = ttk.Entry(config_frame, width=50)
        self.api_key_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Configurar modelo
        ttk.Label(config_frame, text="Modelo:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.model_entry = ttk.Entry(config_frame, width=50)
        self.model_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.model_entry.insert(0, "gemini-pro")

    def setup_files_frame(self):
        files_frame = ttk.LabelFrame(self.main_frame, text="Arquivos")
        files_frame.grid(row=1, column=0, sticky='nsew', padx=5)
        
        button_frame = ttk.Frame(files_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Selecionar PDFs", command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpar Seleção", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        self.files_list = tk.Listbox(files_frame)
        self.files_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_process_button(self):
        self.process_btn = ttk.Button(
            self.main_frame,
            text="Extrair Informações",
            command=self.process_pdfs
        )
        self.process_btn.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    def setup_result_area(self):
        self.result_text = tk.Text(self.main_frame, wrap=tk.WORD)
        self.result_text.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Arquivos PDF", "*.pdf")],
            title="Selecione os PDFs"
        )
        self.selected_files.extend(files)
        self.update_files_list()
        self.logger.info(f"Selecionados {len(files)} arquivos.")

    def clear_files(self):
        self.selected_files.clear()
        self.update_files_list()
        self.logger.info("Lista de arquivos limpa.")

    def update_files_list(self):
        self.files_list.delete(0, tk.END)
        for file in self.selected_files:
            self.files_list.insert(tk.END, os.path.basename(file))

    def check_api_status(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Erro", "Por favor, insira uma API Key do Gemini.")
            return False
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test")
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar com Gemini API: {str(e)}")
            return False

    def split_text_into_chunks(self, text, chunk_size=30000):
        """Divide o texto em chunks respeitando o limite do Gemini."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def analyze_with_gemini(self, text, is_complementary=False):
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            if not is_complementary:
                prompt = f"""Analise detalhadamente este documento que parece ser um contrato ou termo administrativo. 
                Por favor, forneça uma análise estruturada e abrangente incluindo:

                1. IDENTIFICAÇÃO DO DOCUMENTO
                - Tipo de documento
                - Número do contrato/processo
                - Data do documento
                - Sistemas/referências mencionados

                2. PARTES ENVOLVIDAS
                - Detalhes completos do contratante
                - Detalhes completos do contratado
                - Representantes legais e suas qualificações
                - Testemunhas e suas qualificações

                3. OBJETO E ESCOPO
                - Descrição detalhada do objeto
                - Especificações técnicas mencionadas
                - Requisitos especiais
                - Entregáveis esperados

                4. ASPECTOS FINANCEIROS
                - Valor total do contrato
                - Forma de pagamento
                - Dotação orçamentária
                - Condições financeiras especiais

                5. PRAZOS E CRONOGRAMA
                - Prazo de vigência
                - Datas importantes
                - Possibilidades de prorrogação
                - Cronograma de entrega/execução

                6. OBRIGAÇÕES E RESPONSABILIDADES
                - Obrigações detalhadas do contratante
                - Obrigações detalhadas do contratado
                - Responsabilidades específicas
                - Garantias exigidas

                7. ASPECTOS LEGAIS
                - Base legal citada
                - Sanções e penalidades
                - Condições de rescisão
                - Foro e jurisdição

                8. ASPECTOS TÉCNICOS E OPERACIONAIS
                - Especificações técnicas
                - Requisitos de qualidade
                - Procedimentos operacionais
                - Condições de execução

                9. VALIDAÇÃO E ASSINATURAS
                - Detalhes das assinaturas
                - Processo de validação
                - Certificações mencionadas
                - Códigos de verificação

                10. OBSERVAÇÕES IMPORTANTES
                - Pontos críticos identificados
                - Requisitos especiais
                - Informações adicionais relevantes
                - Recomendações de atenção

                Texto para análise:
                {text}
                
                Por favor, apresente a análise de forma clara e organizada, destacando informações críticas e usando formatação para melhor legibilidade. Se alguma das categorias acima não estiver presente no documento, você pode omiti-la."""
            else:
                prompt = f"""Analise este trecho adicional do documento e forneça apenas informações complementares 
                que não foram mencionadas na análise anterior. Foque em:
                
                1. Novos detalhes técnicos
                2. Informações complementares
                3. Especificações adicionais
                4. Outros pontos relevantes não mencionados anteriormente
                
                Texto adicional:
                {text}
                """
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = f"Erro ao analisar com Gemini: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

    def process_pdfs(self):
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            self.logger.warning("Nenhum arquivo selecionado para processamento.")
            return
            
        if not self.check_api_status():
            return
        
        self.process_btn.config(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.logger.info(f"Iniciando processamento de {len(self.selected_files)} PDFs")

        try:
            for pdf_file in self.selected_files:
                try:
                    self.logger.info(f"Processando: {pdf_file}")
                    
                    reader = PdfReader(pdf_file)
                    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

                    # Primeiro, vamos fazer uma análise geral do documento completo
                    self.logger.info("Realizando análise geral do documento")
                    full_analysis = self.analyze_with_gemini(text[:30000], is_complementary=False)
                    
                    self.result_text.insert(tk.END, f"\n=== {os.path.basename(pdf_file)} ===\n")
                    self.result_text.insert(tk.END, "=== ANÁLISE GERAL ===\n")
                    self.result_text.insert(tk.END, full_analysis + "\n")
                    
                    # Se o documento for maior que 30k, vamos fazer análises complementares
                    if len(text) > 30000:
                        chunks = self.split_text_into_chunks(text[30000:], 30000)
                        self.logger.info(f"Realizando análise detalhada de {len(chunks)} partes adicionais")
                        
                        for idx, chunk in enumerate(chunks, 1):
                            self.logger.info(f"Analisando parte adicional {idx}")
                            analysis = self.analyze_with_gemini(chunk, is_complementary=True)
                            self.result_text.insert(tk.END, f"\n=== INFORMAÇÕES COMPLEMENTARES - PARTE {idx} ===\n")
                            self.result_text.insert(tk.END, analysis + "\n")
                    
                    self.result_text.see(tk.END)
                    self.window.update()

                except Exception as e:
                    error_msg = f"Erro ao processar {pdf_file}: {str(e)}"
                    self.result_text.insert(tk.END, error_msg + "\n")
                    self.logger.error(error_msg)
        
        finally:
            self.process_btn.config(state='normal')
            self.logger.info("Processamento de PDFs concluído.")

    def run(self):
        self.logger.info("Iniciando aplicação PDF Analyzer")
        self.window.mainloop()

if __name__ == "__main__":
    app = PDFAnalyzer()
    app.run()