import os
import shutil
from PyPDF2 import PdfReader
import re

def create_folders(base_path):
    folders = [
        'Concorrência', 'Credenciamento', 'Dispensa', 'Inexigibilidade',
        'Leilão', 'Manifestação de Interesse', 'Pregão', 'Outros',
        'Não Lidos', 'Imagens'
    ]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

def extract_text_from_pdf(pdf_path):
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
            
        return text.lower()
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {str(e)}")
        return None

def classify_pdf(text):
    if not text:
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
                return category
    
    return "Outros"

def process_pdfs(input_path):
    create_folders(input_path)
    
    for filename in os.listdir(input_path):
        if not filename.lower().endswith('.pdf'):
            continue
            
        pdf_path = os.path.join(input_path, filename)
        text = extract_text_from_pdf(pdf_path)
        
        if text is None:
            category = "Não Lidos"
        else:
            category = classify_pdf(text)
            
        dest_folder = os.path.join(input_path, category)
        shutil.move(pdf_path, os.path.join(dest_folder, filename))
        print(f"Movido {filename} para {category}")

if __name__ == "__main__":
    input_path = input("Digite o caminho da pasta com os PDFs: ")
    process_pdfs(input_path)
