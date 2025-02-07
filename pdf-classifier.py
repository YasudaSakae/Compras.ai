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
        # Palavras-chave principais com contexto
        self.keywords = {
            'Contratação': {
                'required': [r'\b(contrata[çc][ãa]o|contrato)\b'],
                'context': [r'\bservi[çc]os?\b', r'\bempresa\b', r'\bfornec\w+\b'],
                'exclude': [r'\btermo\s+de\s+refer[êe]ncia\b', r'\bestudo\s+t[ée]cnico\b', 
                          r'\bdocumento\s+de\s+formaliza[çc][ãa]o\b', r'\bmatriz\s+de\s+gerenciamento\b']
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
                'required': [r'\bestudo\s+t[ée]cnico\s+preliminar\b', r'\betp\b'],
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
                'required': [r'\bfunai\b', r'\bfunda[çc][ãa]o\s+nacional\s+dos\s+povos\s+ind[íi]genas\b'],
                'context': [r'\bind[íi]gena\b', r'\bind[íi]genas\b', r'\bpovos\b'],
                'exclude': []
            }
        }
        
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = unidecode(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def calculate_score(self, text: str, category_patterns: Dict) -> float:
        score = 0.0
        
        # Verifica padrões obrigatórios (peso 5.0)
        required_matches = any(re.search(pattern, text) for pattern in category_patterns['required'])
        if not required_matches:
            return 0.0
        score += 5.0
        
        # Verifica contexto (peso 1.0 cada)
        context_matches = sum(1 for pattern in category_patterns['context'] 
                            if re.search(pattern, text))
        score += context_matches * 1.0
        
        # Verifica exclusões (peso -3.0 cada)
        exclude_matches = sum(1 for pattern in category_patterns['exclude'] 
                            if re.search(pattern, text))
        score -= exclude_matches * 3.0
        
        return max(0.0, score)  # Não permite score negativo

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

def extract_text_from_pdf(pdf_path: str, timer: Timer) -> Tuple[str, str, bool]:
    start = time.time()
    try:
        reader = PdfReader(pdf_path)
        if not reader.pages:
            timer.add_time('erro_leitura', time.time() - start)
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
        return "", "", False
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
    
    # Calcula scores para cada categoria
    scores = {}
    for category, patterns in processor.keywords.items():
        # Score do título tem peso 2x
        title_score = processor.calculate_score(cleaned_title, patterns) * 2
        # Score do conteúdo tem peso 1x
        content_score = processor.calculate_score(cleaned_content, patterns)
        # Score final é a soma ponderada
        scores[category] = title_score + content_score
    
    # Encontra a categoria com maior score
    best_match = max(scores.items(), key=lambda x: x[1])
    
    # Se o melhor score for muito baixo (< 5.0), classifica como Outros
    if best_match[1] < 5.0:
        timer.add_time('classificar', time.time() - start)
        return "Outros"
        
    timer.add_time('classificar', time.time() - start)
    return best_match[0]

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
