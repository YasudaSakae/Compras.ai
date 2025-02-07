import os
import shutil
from PyPDF2 import PdfReader
import time
from typing import Dict, List, Tuple, Set
from unidecode import unidecode
import re
from collections import Counter

class Timer:
    def __init__(self):
        self.times: Dict[str, List[float]] = {}
        
    def add_time(self, operation: str, duration: float):
        if operation not in self.times:
            self.times[operation] = []
        self.times[operation].append(duration)
        print(f"Operação '{operation}': {duration:.3f}s")
        
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
    
    def extract_meaningful_words(self, text: str) -> List[str]:
        # Remove pontuação e números
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        # Divide em palavras e remove stopwords
        words = [w for w in text.split() if len(w) > 2]
        return words
    
    def get_text_signature(self, text: str) -> Counter:
        words = self.extract_meaningful_words(text)
        return Counter(words)

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

def extract_text_from_pdf(pdf_path: str, timer: Timer) -> Tuple[str, str, bool]:
    start = time.time()
    try:
        reader = PdfReader(pdf_path)
        if not reader.pages:
            return "", "", False
            
        # Extrai título (primeiras 10 palavras da primeira página)
        first_page = reader.pages[0].extract_text()
        title = ' '.join(first_page.split()[:10])
        
        # Extrai conteúdo normal
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
        print(f"Erro na leitura de {pdf_path}: {str(e)}")
        timer.add_time('erro_leitura', time.time() - start)
        return "", False

def classify_pdf(title: str, content: str, processor: TextProcessor, timer: Timer) -> str:
    start = time.time()
    if not content and not title:
        timer.add_time('classificar', time.time() - start)
        return "Imagens"
    
    # Limpa os textos
    cleaned_title = processor.clean_text(title)
    cleaned_content = processor.clean_text(content)
    
    # Verifica primeiro no título
    title_matches = {}
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
    
    # Encontra a categoria com mais matches no conteúdo
    best_match = max(content_matches.items(), key=lambda x: x[1])
    timer.add_time('classificar', time.time() - start)
    
    return best_match[0] if best_match[1] > 0 else "Outros"

def process_pdfs(input_path: str) -> None:
    timer = Timer()
    processor = TextProcessor()
    total_start = time.time()
    
    create_folders(input_path, timer)
    
    stats = {'processed': 0, 'moved': {}}
    for filename in os.listdir(input_path):
        if not filename.lower().endswith('.pdf'):
            continue
            
        stats['processed'] += 1
        pdf_path = os.path.join(input_path, filename)
        
        title, content, success = extract_text_from_pdf(pdf_path, timer)
        category = "Não Lidos" if not success else classify_pdf(title, content, processor, timer)
        
        dest_folder = os.path.join(input_path, category)
        try:
            start = time.time()
            shutil.move(pdf_path, os.path.join(dest_folder, filename))
            timer.add_time('mover_arquivo', time.time() - start)
            stats['moved'][category] = stats['moved'].get(category, 0) + 1
            print(f"Movido: {filename} → {category}")
        except Exception as e:
            print(f"Erro ao mover {filename}: {str(e)}")
    
    print_statistics(timer, stats, time.time() - total_start)

def print_statistics(timer: Timer, stats: Dict, total_time: float) -> None:
    print("\nEstatísticas de Tempo (segundos):")
    for op, metrics in timer.get_stats().items():
        print(f"\n{op.upper()}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.3f}")
    
    if stats['processed'] > 0:
        print(f"\nProcessamento:")
        print(f"Total de arquivos: {stats['processed']}")
        print(f"Tempo médio/arquivo: {total_time/stats['processed']:.3f}s")
        print("\nDistribuição por categoria:")
        for category, count in stats['moved'].items():
            print(f"{category}: {count}")

if __name__ == "__main__":
    input_path = input("Caminho da pasta com PDFs: ").strip()
    process_pdfs(input_path)
