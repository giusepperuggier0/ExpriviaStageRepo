import re
import os
import pandas as pd
import json
from typing import List, Dict, Union

def extract_info_from_cv(file_path: str) -> Dict[str, Union[str, List[str]]]:
    """Estrae le informazioni da un singolo file CV"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Estrazione nome e cognome (prima riga dopo "Curriculum X")
    name_line = text.split('\n')[2].strip()
    name_parts = name_line.split()
    name = " ".join(name_parts[:-1]) if len(name_parts) > 1 else name_parts[0]
    surname = name_parts[-1] if name_parts else ""
    
    # Estrazione email
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = email.group() if email else ""
    
    # Estrazione telefono
    phone = re.search(r'\+?\d[\d\s-]{7,}\d', text)
    phone = phone.group().strip() if phone else ""
    
    # Estrazione data di nascita
    dob = re.search(r'Date of Birth:\s*(\d{4})', text)
    dob = dob.group(1) if dob else ""
    
    # Estrazione esperienza lavorativa più recente (versione migliorata)
    recent_work = ""
    if "WORK EXPERIENCE:" in text:
        work_section = text.split("WORK EXPERIENCE:")[1]
        # Dividi per sezioni (due newline)
        sections = [s.strip() for s in work_section.split('\n\n') if s.strip()]
        if sections:
            # Prendi la prima sezione (esperienza più recente)
            recent_work = sections[0]
            # Mantieni solo le prime 3 righe per semplificare
            recent_work = '\n'.join(recent_work.split('\n')[:3])
    
    # Estrazione skills di lavoro
    work_skills = []
    if "SKILLS:" in text:
        skills_section = text.split("SKILLS:")[1].split("\n\n")[0]
        work_skills = [s.strip('- ').strip() for s in skills_section.split('\n') if s.strip()]
    
    # Estrazione skills linguistiche
    language_skills = []
    if "LANGUAGE SKILLS:" in text:
        lang_section = text.split("LANGUAGE SKILLS:")[1].split("\n\n")[0]
        language_skills = [s.strip('- ').strip() for s in lang_section.split('\n') if s.strip()]
    
    return {
        'name': name,
        'surname': surname,
        'email': email,
        'phone': phone,
        'date_of_birth': dob,
        'recent_work_experience': recent_work,
        'work_skills': work_skills,
        'language_skills': language_skills,
        'source_file': os.path.basename(file_path)
    }

def process_cv_directory(directory: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Processa tutti i file CV in una directory"""
    cv_data = []
    for filename in sorted(os.listdir(directory)):
        if filename.startswith('cv_') and filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                cv_info = extract_info_from_cv(file_path)
                cv_data.append(cv_info)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    return cv_data

def save_to_dataframe_and_json(cv_data: List[Dict], json_output: str):
    """Salva i dati in DataFrame e JSON"""
    # Crea DataFrame
    df = pd.DataFrame(cv_data)
    
    # Riordina le colonne
    columns_order = [
        'source_file', 'name', 'surname', 'email', 'phone', 'date_of_birth',
        'recent_work_experience', 'work_skills', 'language_skills'
    ]
    df = df[columns_order]
    
    # Salva in JSON
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(cv_data, f, indent=4, ensure_ascii=False)
    
    return df

if __name__ == "__main__":
    # Configurazione percorsi
    cv_directory = "C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Pdf_extr/Curriculum_skills"
    output_json = "C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Pdf_extr/json/cv_data.json"
    
    # Elabora i file CV
    cv_data = process_cv_directory(cv_directory)
    
    # Salva i risultati
    df = save_to_dataframe_and_json(cv_data, output_json)
    
    # Stampa il DataFrame
    print("\nEstratto DataFrame:")
    print(df)
    
    # Salva DataFrame come CSV
    df.to_csv("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Pdf_extr/csv/cv_data.csv", index=False)
    print("\nDati salvati in JSON e CSV")