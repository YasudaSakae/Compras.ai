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
                'required': [
                    r'\baviso\s+de\s+licita[çc][ãa]o\b',
                    r'\bedital\s+de\s+licita[çc][ãa]o\b',
                    r'\bprocesso\s+licitat[óo]rio\b',
                    r'\bcontrata[çc][ãa]o\s+direta\b'
                ],
                'context': [
                    r'\bempresa\b',
                    r'\bvalor\s+estimado\b',
                    r'\bvalor\s+total\b',
                    r'\bcnpj\b',
                    r'\bproposta\b',
                    r'\bservi[çc]os?\b',
                    r'\bcontratante\b',
                    r'\bcontratada\b',
                    r'\blicita[çc][ãa]o\b'
                ],
                'exclude': [
                    r'\btermo\s+de\s+refer[êe]ncia\b',
                    r'\bestudo\s+t[ée]cnico\b',
                    r'\bestudos?\s+preliminares?\b',
                    r'\bdocumento\s+de\s+formaliza[çc][ãa]o\b',
                    r'\bmatriz\s+de\s+gerenciamento\b',
                    r'\bparecer\b',
                    r'\bdespacho\b',
                    r'\bata\s+de\s+reuni[ãa]o\b',
                    r'\bmem[óo]ria\s+de\s+reuni[ãa]o\b',
                    r'\brelat[óo]rio\b',
                    r'\banexo\b',
                    r'\bformul[áa]rio\b'
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
    
    def calculate_score(self, text: str, category_patterns: Dict) -> float:
        score = 0.0
        
        # Verifica padrões obrigatórios (peso 5.0)
        required_matches = sum(1 for pattern in category_patterns['required'] 
                             if re.search(pattern, text))
        
        # Para a categoria Contratação, exige pelo menos 2 matches de required
        if 'contratação' in text.lower() and required_matches < 2:
            return 0.0
            
        if required_matches == 0:
            return 0.0
        score += required_matches * 5.0
        
        # Verifica contexto (peso 1.0 cada)
        context_matches = sum(1 for pattern in category_patterns['context'] 
                            if re.search(pattern, text))
        
        # Para Contratação, exige pelo menos 3 palavras de contexto
        if 'contratação' in text.lower() and context_matches < 3:
            return 0.0
            
        score += context_matches * 1.0
        
        # Verifica exclusões (peso -3.0 cada)
        exclude_matches = sum(1 for pattern in category_patterns['exclude'] 
                            if re.search(pattern, text))
        score -= exclude_matches * 3.0
        
        # Penalidade extra para exclusões na categoria Contratação
        if 'contratação' in text.lower():
            score -= exclude_matches * 2.0  # Penalidade adicional
            
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

def classify_pdf(title: str, content: str, processor: TextProcessor, timer: Timer, regex_cache: Dict) -> str:
    start = time.time()
    if not content and not title:
        timer.add_time('classificar', time.time() - start)
        return "Imagens"
    
    # Limpa os textos
    cleaned_title = processor.clean_text(title)
    cleaned_content = processor.clean_text(content)
    
    # Combina título e conteúdo com pesos diferentes
    full_text = cleaned_title * 2 + " " + cleaned_content
    
    # Calcula scores usando regex pré-compilados
    scores = {}
    for category, patterns in regex_cache.items():
        score = 0.0
        
        # Verifica padrões obrigatórios (peso 5.0)
        required_matches = sum(1 for pattern in patterns['required'] 
                             if pattern.search(full_text))
        
        # Regras específicas para Contratação
        if category.lower() == 'contratação':
            if required_matches < 2:
                continue
        elif required_matches == 0:
            continue
            
        score += required_matches * 5.0
        
        # Verifica contexto (peso 1.0 cada)
        context_matches = sum(1 for pattern in patterns['context'] 
                            if pattern.search(full_text))
        
        # Regras específicas para Contratação
        if category.lower() == 'contratação' and context_matches < 3:
            continue
            
        score += context_matches * 1.0
        
        # Verifica exclusões (peso -3.0 cada)
        exclude_matches = sum(1 for pattern in patterns['exclude'] 
                            if pattern.search(full_text))
        score -= exclude_matches * 3.0
        
        # Penalidade extra para Contratação
        if category.lower() == 'contratação':
            score -= exclude_matches * 2.0
            
        if score > 0:
            scores[category] = score
    
    if not scores:
        timer.add_time('classificar', time.time() - start)
        return "Outros"
        
    # Encontra a categoria com maior score
    best_match = max(scores.items(), key=lambda x: x[1])
    
    timer.add_time('classificar', time.time() - start)
    return best_match[0]

def process_pdfs(input_path: str) -> None:
    timer = Timer()
    processor = TextProcessor()
    total_start = time.time()
    
    create_folders(input_path, timer)
    
    # Pre-compilar expressões regulares
    regex_cache = {}
    for category, patterns in processor.keywords.items():
        regex_cache[category] = {
            'required': [re.compile(pattern) for pattern in patterns['required']],
            'context': [re.compile(pattern) for pattern in patterns['context']],
            'exclude': [re.compile(pattern) for pattern in patterns['exclude']]
        }
    
    stats = {'processed': 0, 'moved': {}, 'errors': 0}
    
    # Processar arquivos em lotes para melhor performance
    batch_size = 50
    pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
    
    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i + batch_size]
        
        for filename in batch:
            try:
                pdf_path = os.path.join(input_path, filename)
                stats['processed'] += 1
                
                # Adiciona verificação de arquivo corrompido
                if os.path.getsize(pdf_path) < 100:  # arquivos muito pequenos provavelmente estão corrompidos
                    print(f"Arquivo muito pequeno (possivelmente corrompido): {filename}")
                    category = "Não Lidos"
                else:
                    title, content, success = extract_text_from_pdf(pdf_path, timer)
                    category = "Não Lidos" if not success else classify_pdf(title, content, processor, timer, regex_cache)
                
                dest_folder = os.path.join(input_path, category)
                try:
                    start = time.time()
                    shutil.move(pdf_path, os.path.join(dest_folder, filename))
                    timer.add_time('mover_arquivo', time.time() - start)
                    stats['moved'][category] = stats['moved'].get(category, 0) + 1
                    print(f"Processado ({stats['processed']}/{len(pdf_files)}): {filename} → {category}")
                except Exception as e:
                    print(f"Erro ao mover {filename}: {str(e)}")
                    stats['errors'] += 1
                    
            except Exception as e:
                print(f"Erro ao processar {filename}: {str(e)}")
                stats['errors'] += 1
                continue
        
        # Limpa a memória periodicamente
        if i % (batch_size * 5) == 0:
            import gc
            gc.collect()
    
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
