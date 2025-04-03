import re
import pdfplumber
import spacy
import pandas as pd
from spacy.training.example import Example
import json
from spacy import displacy
from pathlib import Path

def clean_annotations(annotations, text):
    cleaned = []
    for start, end, label in annotations:
        if (isinstance(label, str) and 
            0 <= start < end <= len(text) and
            not any(s < end and e > start for s, e, _ in cleaned)):
            cleaned.append((start, end, label.upper()))
    return cleaned

def train_spacy_model(train_data_path, output_dir=None, n_iter=27):
    
    nlp = spacy.blank("en")
    
    # Aggiungi il componente NER
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
    
    # Prepara i dati di addestramento
    training_data = []
    with open(train_data_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                text = data["text"]
                annotations = data["label"]
                
                # Pulisci e verifica le annotazioni
                cleaned_annotations = clean_annotations(annotations, text)
                
                # Aggiungi al training data solo se ci sono annotazioni valide
                if cleaned_annotations:
                    training_data.append((text, {"entities": cleaned_annotations}))
                    
                    # Aggiungi le etichette al NER
                    for _, _, label in cleaned_annotations:
                        ner.add_label(label)
            except json.JSONDecodeError as e:
                print(f"Errore nel parsing della linea: {line}. Errore: {e}")
                continue
    
    
    if not training_data:
        raise ValueError("Nessun dato di addestramento valido trovato.") 
    
    # Addestra il modello
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # Disabilita gli altri componenti durante l'addestramento
        optimizer = nlp.begin_training()
        
        for itn in range(n_iter):
            losses = {}
            for text, annotations in training_data:
                try:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    nlp.update([example], drop=0.5, losses=losses, sgd=optimizer)
                except Exception as e:
                    print(f"Errore durante l'addestramento con il testo: {text[:20]}...")
                    print(f"Errore: {e}")
                    continue
            
            print(f"Iteration {itn + 1}, Losses: {losses}")
    
    # Salva il modello se richiesto
    if output_dir:
        output_path = Path(output_dir)
        if not output_path.exists():
            output_path.mkdir()
        nlp.to_disk(output_dir)
        print(f"Modello salvato in {output_dir}")
    
    return nlp

def process_pdf(pdf_path, nlp):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    print("\n=== Analisi del testo ===")
    print(text[0:100])

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    df = pd.DataFrame(entities, columns=['text', 'type'])
    
    print("\n=== Entità Trovate ===")
    print(df.head(20))
    
    return df, text, doc

def extract_info(df, doc, text):
    info = {
        'name': "",
        'surname': "",
        'address': "",
        'email': [],
        'phone': [],
        'date_of_birth': "",
        'work_experience': []
    }
    
    # Estrazione Cognome e poi Nome
    surname_entries = df[df['type'] == 'COGNOME']['text'].values
    if len(surname_entries) > 0:
        info['surname'] = surname_entries[0]
        name_surname_pattern = re.compile(
            r'(\b[A-Z][a-z]+\b)\s+' + re.escape(info['surname']),  
            re.IGNORECASE
        )
        match = name_surname_pattern.search(text)
        if match:
            info['name'] = match.group(1)

    
    
    # Estrazione indirizzo
    address_candidates = df[df['type'].str.upper() == 'LIVES']['text'].values
    info['address'] = None  # Initialize as None
    for addr in address_candidates:
        if re.search(r'\d+.*[A-Za-z]+,.*\d{2,}', addr):  
            info['address'] = addr
            break
    if info['address'] is None and len(address_candidates) > 0:
        info['address'] = address_candidates[0]
    
    #Email
    email_entries = [email for email in df[df['type'].str.upper() == 'EMAIL']['text'].tolist() 
                    if '@' in email]
    info['email'] = email_entries 
    
    # Estrazione data di nascita
    dob_entries = df[df['type'].str.upper() == 'DBO']['text'].values
    if len(dob_entries) > 0:
        date_match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', dob_entries[0])
        if date_match:
            info['date_of_birth'] = date_match.group()
        else:
            info['date_of_birth'] = dob_entries[0]  
    
    #Telefono
    phone_entries = df[df['type'].str.upper() == 'PHONE']['text'].tolist()
    if not phone_entries:
        potential_phones = df[df['text'].str.contains(r'\+[\d\s]{8,}', regex=True)]['text'].tolist()
        phone_entries = potential_phones
    cleaned_phones = []
    for phone in phone_entries:
        digits = re.sub(r'[^\d+]', '', phone)
        if len(digits) >= 8:  
            cleaned_phones.append(digits)
    info['phone'] = cleaned_phones if cleaned_phones else ["Non disponibile"]
    

    #Work
    work_entries = df[
        (df['type'].str.upper() == 'WORK') | 
        (df['text'].str.contains(r'present|current|now|today', case=False))
    ]['text'].tolist()
    current_work = [
        work for work in work_entries 
        if re.search(r'current|present|now|today', work, re.IGNORECASE)
    ]
    if not current_work and work_entries:
        current_work = [work_entries[0]]  
        
    info['work_experience'] = current_work
                
    return info

def print_and_save_info(info, json_filename="C:\\Users\\Giuseppe\\Desktop\\Stage_exprivia\\Python\\Pdf_extr\\json\\extracted_info.json"):
    print(f"Nome: {info['name']}")
    print(f"Cognome: {info['surname']}")
    print(f"Via : {info['address']}")
    print(f"Data di nascita: {info['date_of_birth']}")
    print(f"Email: {', '.join(info['email'])}")
    print(f"Telefono: {', '.join(info['phone'])}")
    print("Ultima Esperienza di Lavoro:")
    for exp in info['work_experience']:
        print(f"- {exp}")
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    
    print(f"\nInformation saved to {json_filename}")


train_data_path = "C:\\Users\\Giuseppe\\Downloads\\d30addda-60b5-4fa8-a926-8ccd5bf8e3a7\\admin.json"
pdf_path = "C:\\Users\\Giuseppe\\Desktop\\Stage_exprivia\\Python\\Pdf_extr\\Curriculum_pdf\\EuropassCV.pdf"

try:
    nlp = spacy.load("test_model")
    print("Modello esistente")
except OSError:
    print("Allenamento del modello")
    nlp = train_spacy_model(train_data_path, output_dir="test_model")


try:
    df, text, doc = process_pdf(pdf_path, nlp)
    info = extract_info(df, doc, text)
    print_and_save_info(info)
    
    
    #displacy.serve(doc, style="ent")
except Exception as e:
    print(f"Errore durante l'elaborazione del PDF: {e}")