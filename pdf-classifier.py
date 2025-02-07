import os
import shutil
from PyPDF2 import PdfReader
import time
from typing import Dict, List, Tuple
from unidecode import unidecode  # Importando unidecode para remover acentos
import re  # Importando para usar expressões regulares

class Timer:
    def __init__(self):
        self.times: Dict[str, List[float]] = {}
        
    def add_time(self, operation: str, duration: float):
        if operation not in self.times:
            self.times[operation] = []
        self.times[operation].append(duration)
        print(f"Tempo de operação '{operation}': {duration:.3f} segundos")  # Log da operação
        
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
        'Contratação', 'Credenciamento', 'Dispensa', 'Inexigibilidade',
        'Leilão', 'Manifestação de Interesse', 'Pregão', 'Outros',
        'Não Lidos', 'Imagens', 'Termo de Referência', 'Estudo Técnico Preliminar',
        'Matriz de Gerenciamento de Riscos'
    ]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Diretório '{folder}' criado em {folder_path}")
    timer.add_time('criar_pastas', time.time() - start)
    print("\nEstatísticas parciais:")
    stats = timer.get_stats()
    for operation, metrics in stats.items():
        print(f"\n{operation.upper()}:")
        print(f"  Média: {metrics['média']:.3f}")
        print(f"  Mínimo: {metrics['min']:.3f}")
        print(f"  Máximo: {metrics['max']:.3f}")
        print(f"  Total: {metrics['total']:.3f}")

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
        
    # Aplicando unidecode para remover acentos antes da comparação
    normalized_text = unidecode(text).lower()

    keywords = {
        'Contratação': [r'\bcontratação\b', r'\bcontratacao\b'],  # Regex para palavras completas
        'Credenciamento': [r'\bcredenciamento\b'],
        'Dispensa': [r'\bdispensa\b'],
        'Inexigibilidade': [r'\binexigibilidade\b'],
        'Leilão': [r'\bleilão\b', r'\bleilao\b'],
        'Manifestação de Interesse': [r'\bmanifestação de interesse\b', r'\bmanifestacao de interesse\b'],
        'Pregão': [r'\bpregão\b', r'\bpregao\b'],
        'Termo de Referência': [r'\btermo de referência\b', r'\btr\b', r'\bTermo de Referência\b'],
        'Estudo Técnico Preliminar': [r'\bestudo técnico preliminar\b', r'\bestudo tecnico preliminar\b'],
        'Matriz de Gerenciamento de Riscos': [r'\bmatriz de gerenciamento de riscos\b']
    }
    
    # Checando se algum dos termos de uma categoria está no texto
    for category, terms in keywords.items():
        for term in terms:
            # Usando regex para verificar a presença de uma expressão completa
            if re.search(term, normalized_text):
                # Verificando se a categoria encontrada tem mais de uma correspondência
                if len(re.findall(term, normalized_text)) > 1:
                    timer.add_time('classificar', time.time() - start)
                    return category
    
    timer.add_time('classificar', time.time() - start)
    return "Outros"

def move_file(source: str, dest_folder: str, filename: str, timer: Timer, move_count: Dict[str, int]):
    start = time.time()
    shutil.move(source, os.path.join(dest_folder, filename))
    
    # Incrementa a contagem de arquivos movidos para a pasta correspondente
    if dest_folder not in move_count:
        move_count[dest_folder] = 0
    move_count[dest_folder] += 1
    
    timer.add_time('mover_arquivo', time.time() - start)

def process_pdfs(input_path: str):
    timer = Timer()
    total_start = time.time()
    
    create_folders(input_path, timer)
    
    files_processed = 0
    move_count = {}  # Dicionário para contar arquivos movidos por pasta
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
        move_file(pdf_path, dest_folder, filename, timer, move_count)
        print(f"Movido {filename} para {category}")
    
    total_time = time.time() - total_start
    timer.add_time('tempo_total', total_time)
    
    # Imprime estatísticas de tempo detalhadas
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
    
    # Imprime o número de arquivos movidos para cada pasta
    print("\nResumo de arquivos movidos para cada pasta:")
    for folder, count in move_count.items():
        print(f"{folder}: {count} arquivo(s)")

if __name__ == "__main__":
    input_path = input("Digite o caminho da pasta com os PDFs: ")
    process_pdfs(input_path)
