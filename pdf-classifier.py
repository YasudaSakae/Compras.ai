import os
import shutil
from PyPDF2 import PdfReader
import time
from typing import Dict, List, Tuple, Set
from unidecode import unidecode
import re
from collections import Counter
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
            'Contratação': {
                'required': [
                    r'\b(contrata[çc][ãa]o|contrato)\b',
                    r'\baviso\s+de\s+licita[çc][ãa]o\b',
                    r'\bedital\s+de\s+licita[çc][ãa]o\b',
                    r'\bprocesso\s+licitat[óo]rio\b',
                    r'\bcontrata[çc][ãa]o\s+direta\b',
                    r'\bextrato\s+de\s+contrato\b',
                    r'\bextrato\s+contratual\b'
                ],
                'context': [
                    r'\bempresa\b',
                    r'\bvalor\b',
                    r'\bcnpj\b',
                    r'\bproposta\b',
                    r'\bservi[çc]os?\b',
                    r'\bcontratante\b',
                    r'\bcontratada\b',
                    r'\blicita[çc][ãa]o\b',
                    r'\bfornec\w+\b',
                    r'\baquisição\b',
                    r'\bpregão\b',
                    r'\bconcorrência\b'
                ],
                'exclude': [
                    r'\btermo\s+de\s+refer[êe]ncia\b',
                    r'\bestudo\s+t[ée]cnico\b',
                    r'\bestudos?\s+preliminares?\b',
                    r'\bdocumento\s+de\s+formaliza[çc][ãa]o\b',
                    r'\bmatriz\s+de\s+gerenciamento\b'
                ]
            },
            'Dispensa': {
                'required': [r'\bdispensa\b'],
                'context': [r'\blicita[çc][ãa]o\b', r'\bcontrata[çc][ãa]o\s+direta\b'],
                'exclude': []
            },
            'Termo de Referência': {
                'required': [r'\btermo\s+de\s+refer[êe]ncia\b', r'\btr\b'],
                'context': [r'\bespecifica[çc][õo]es\b', r'\brequisitos\b'],
                'exclude': []
            },
            'Estudo Técnico Preliminar': {
                'required': [r'\bestudo\s+t[ée]cnico\s+preliminar\b', r'\betp\b', r'\bestudos?\s+preliminares?\b'],
                'context': [r'\bplanejamento\b', r'\bviabilidade\b'],
                'exclude': []
            },
            'Matriz de Gerenciamento de Riscos': {
                'required': [r'\bmatriz\s+de\s+gerenciamento\s+de\s+riscos\b', r'\bmatriz\s+de\s+riscos\b'],
                'context': [r'\bimpacto\b', r'\bprobabilidade\b', r'\bconting[êe]ncia\b'],
                'exclude': []
            },
            'DFD': {
                'required': [r'\bdocumento\s+de\s+formaliza[çc][ãa]o\s+da\s+demanda\b', r'\bdfd\b'],
                'context': [r'\bdemanda\b', r'\bformaliza[çc][ãa]o\b', r'\brequisitante\b'],
                'exclude': []
            },
            'FUNAI': {
                'required': [r'\bfunai\b', r'\bfunda[çc][ãa]o\s+nacional\s+dos\s+povos\s+ind[íi]genas\b', r'\bfunda[çc][ãa]o\s+nacional\s+dos?\s+[íi]ndios?\b'],
                'context': [r'\bind[íi]gena\b', r'\bind[íi]genas\b', r'\bpovos\b'],
                'exclude': []
            }
        }
        
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = unidecode(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

def create_folders(base_path: str, timer: Timer) -> None:
    start = time.time()
    folders = [
        'Contratação', 'Dispensa', 'Outros', 'Não Lidos', 'Imagens',
        'Termo de Referência', 'Estudo Técnico Preliminar',
        'Matriz de Gerenciamento de Riscos', 'DFD', 'FUNAI'
    ]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    timer.add_time('criar_pastas', time.time() - start)

@timeout(10)
def extract_text_from_pdf(pdf_path: str, timer: Timer) -> Tuple[str, str, bool]:
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
        print(f"Erro na leitura de {pdf_path}: {str(e)}")
        timer.add_time('erro_leitura', time.time() - start)
        return "", "", False

@timeout(10)
def classify_pdf(title: str, content: str, processor: TextProcessor, timer: Timer, regex_cache: Dict) -> str:
    start = time.time()
    if not content and not title:
        timer.add_time('classificar', time.time() - start)
        return "Imagens"
    
    cleaned_title = processor.clean_text(title)
    cleaned_content = processor.clean_text(content)
    full_text = cleaned_title * 2 + " " + cleaned_content
    
    scores = {}
    for category, patterns in regex_cache.items():
        score = 0.0
        required_matches = sum(1 for pattern in patterns['required'] 
                             if pattern.search(full_text))
        
        if category.lower() == 'contratação':
            if required_matches < 1:
                continue
        elif required_matches == 0:
            continue
            
        score += required_matches * 5.0
        
        context_matches = sum(1 for pattern in patterns['context'] 
                            if pattern.search(full_text))
        
        if category.lower() == 'contratação' and context_matches < 2:
            continue
            
        score += context_matches * 1.0
        
        exclude_matches = sum(1 for pattern in patterns['exclude'] 
                            if pattern.search(full_text))
        score -= exclude_matches * 3.0
        
        if category.lower() == 'contratação':
            score -= exclude_matches * 2.0
            
        if score > 0:
            scores[category] = score
    
    if not scores:
        timer.add_time('classificar', time.time() - start)
        return "Outros"
        
    best_match = max(scores.items(), key=lambda x: x[1])
    
    timer.add_time('classificar', time.time() - start)
    return best_match[0]

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
        total_files = sum(stats['moved'].values())
        for category, count in stats['moved'].items():
            percentage = (count / total_files) * 100
            print(f"{category}: {count} ({percentage:.1f}%)")
        
        if stats['errors'] > 0:
            error_percentage = (stats['errors'] / stats['processed']) * 100
            print(f"\nErros: {stats['errors']} ({error_percentage:.1f}%)")

def process_pdfs(input_path: str) -> None:
    timer = Timer()
    processor = TextProcessor()
    total_start = time.time()
    
    create_folders(input_path, timer)
    
    regex_cache = {}
    for category, patterns in processor.keywords.items():
        regex_cache[category] = {
            'required': [re.compile(pattern) for pattern in patterns['required']],
            'context': [re.compile(pattern) for pattern in patterns['context']],
            'exclude': [re.compile(pattern) for pattern in patterns['exclude']]
        }
    
    stats = {'processed': 0, 'moved': {}, 'errors': 0}
    batch_size = 50
    pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
    
    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i + batch_size]
        
        for filename in batch:
            try:
                pdf_path = os.path.join(input_path, filename)
                stats['processed'] += 1
                
                if os.path.getsize(pdf_path) < 100:
                    print(f"Arquivo muito pequeno (possivelmente corrompido): {filename}")
                    category = "Não Lidos"
                else:
                    result = extract_text_from_pdf(pdf_path, timer)
                    if result is None:  # Timeout occurred
                        category = "Não Lidos"
                    else:
                        title, content, success = result
                        if not success:
                            category = "Não Lidos"
                        else:
                            classification_result = classify_pdf(title, content, processor, timer, regex_cache)
                            category = "Não Lidos" if classification_result is None else classification_result
                
                dest_folder = os.path.join(input_path, category)
                try:
                    start = time.time()
                    shutil.move(pdf_path, os.path.join(dest_folder, filename))
                    timer.add_time('mover_arquivo', time.time() - start)
                    stats['moved'][category] = stats['moved'].get(category, 0) + 1
                    
                    progress_percent = (stats['processed'] / len(pdf_files)) * 100
                    print(f"Processado ({stats['processed']}/{len(pdf_files)} - {progress_percent:.1f}%): {filename} → {category}")
                    
                except Exception as e:
                    print(f"Erro ao mover {filename}: {str(e)}")
                    stats['errors'] += 1
                    
            except Exception as e:
                print(f"Erro ao processar {filename}: {str(e)}")
                stats['errors'] += 1
                continue
        
        if i % (batch_size * 5) == 0:
            import gc
            gc.collect()
    
    print_statistics(timer, stats, time.time() - total_start)

if __name__ == "__main__":
    input_path = input("Caminho da pasta com PDFs: ").strip()
    process_pdfs(input_path)
