import re
import pdfplumber
import spacy
import pandas as pd
from spacy.training.example import Example
import json
from spacy import displacy
from pathlib import Path
import os
import random
from spacy.util import minibatch, compounding

def clean_annotations(annotations, text):
    cleaned = []
    for start, end, label in annotations:
        # Normalizza le etichette
        label = label.upper().replace("SKILL-", "SKILLS-")
        label = "NAME" if label == "NOME" else label
        label = "SURNAME" if label == "COGNOME" else label
        label = "DOB" if label == "DBO" else label
        
        if (isinstance(label, str)) and 0 <= start < end <= len(text):
            # Pulisci il testo estratto
            entity_text = text[start:end]
            if label == "DOB":
                entity_text = re.search(r'\d{4}', entity_text).group() if re.search(r'\d{4}', entity_text) else ""
            cleaned.append((start, end, label))
    return cleaned

def train_spacy_model(train_data_path, output_dir=None, n_iter=30):
    nlp = spacy.blank("en")
    
    # Configurazione personalizzata per il NER
    config = {
        "moves": None,
        "update_with_oracle_cut_size": 100,
        "model": {
            "@architectures": "spacy.TransitionBasedParser.v2",
            "state_type": "ner",
            "extra_state_tokens": False,
            "hidden_width": 64,
            "maxout_pieces": 2,
            "use_upper": False
        }
    }
    
    ner = nlp.add_pipe("ner", config=config)
    
    # Aggiungi tutte le etichette possibili
    labels = {"NAME", "SURNAME", "LIVES", "PHONE", "EMAIL", "DOB", "WORK", "SKILLS-L", "SKILLS-SS"}
    for label in labels:
        ner.add_label(label)
    
    # Carica e prepara i dati di addestramento
    training_examples = []
    with open(train_data_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                text = data["text"]
                annotations = clean_annotations(data["label"], text)
                
                # Crea esempio di addestramento
                entities = {"entities": annotations}
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, entities)
                training_examples.append(example)
            except json.JSONDecodeError as e:
                print(f"Errore nel parsing della linea: {line}. Errore: {e}")
                continue
    
    if not training_examples:
        raise ValueError("Nessun dato di addestramento valido trovato.")
    
    # Addestramento con ottimizzazioni
    optimizer = nlp.initialize()
    
    for itn in range(n_iter):
        losses = {}
        random.shuffle(training_examples)
        batches = minibatch(training_examples, size=compounding(4.0, 32.0, 1.001))
        
        for batch in batches:
            nlp.update(batch, drop=0.35, losses=losses, sgd=optimizer)
        
        print(f"Iteration {itn + 1}, Losses: {losses}")
    
    if output_dir:
        output_path = Path(output_dir)
        if not output_path.exists():
            output_path.mkdir()
        nlp.to_disk(output_dir)
        print(f"Modello salvato in {output_dir}")
    
    return nlp

def preprocess_text(text):
    # Unisci linee vuote multiple
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Rimuovi spazi multipli
    text = re.sub(r' +', ' ', text)
    return text.strip()

def process_txt_files(txt_directory, nlp):
    txt_files = [f for f in os.listdir(txt_directory) if f.endswith('.txt') and f.startswith('cv_')]
    
    all_extracted_data = []
    
    for txt_file in sorted(txt_files, key=lambda x: int(x.split('_')[1].split('.')[0])):
        file_path = os.path.join(txt_directory, txt_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = preprocess_text(f.read())
        
        print(f"\n=== Processing {txt_file} ===")
        
        # Approccio ibrido: usa sia NER che regex
        hybrid_info = extract_info_from_text(text)
        doc = nlp(text)
        
        # Combina i risultati
        combined_info = {
            'file': txt_file,
            'name': hybrid_info['name'] or get_entity_text(doc, 'NAME'),
            'surname': hybrid_info['surname'] or get_entity_text(doc, 'SURNAME'),
            'phone': hybrid_info['phone'] or get_entity_text(doc, 'PHONE', True),
            'email': hybrid_info['email'] or get_entity_text(doc, 'EMAIL', True),
            'lives': hybrid_info['lives'] or get_entity_text(doc, 'LIVES'),
            'work': hybrid_info['work'] or get_entity_text(doc, 'WORK', True),
            'dob': hybrid_info['dob'] or get_entity_text(doc, 'DOB'),
            'skills-l': hybrid_info['skills-l'] or get_entity_text(doc, 'SKILLS-L', True),
            'skills-ss': hybrid_info['skills-ss'] or get_entity_text(doc, 'SKILLS-SS', True)
        }
        
        all_extracted_data.append(combined_info)
    
    return all_extracted_data

def get_entity_text(doc, label, as_list=False):
    entities = [ent.text for ent in doc.ents if ent.label_ == label]
    if as_list:
        return entities
    return entities[0] if entities else ""

def extract_info_from_text(text):
    # Estrazione email (regex affidabile)
    emails = list(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)))
    
    # Estrazione telefono (regex migliorata)
    phones = list(set(re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,3}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}', text)))
    phones = [re.sub(r'[^\d+]', '', phone) for phone in phones if len(re.sub(r'[^\d+]', '', phone)) >= 8]
    
    # Estrazione nome e cognome (pattern specifico)
    name_line = text.split('\n')[1] if len(text.split('\n')) > 1 else ""
    name_parts = re.findall(r'[A-Z][a-z]+', name_line)
    
    # Estrazione indirizzo (riga dopo nome)
    address_line = text.split('\n')[2] if len(text.split('\n')) > 2 else ""
    
    # Estrazione data di nascita
    dob_match = re.search(r'Date of Birth:\s*(\d{2}[/-]\d{2}[/-]\d{4}|\d{4})', text, re.IGNORECASE)
    
    # Estrazione skills (sezioni specifiche)
    skills_l = []
    skills_ss = []
    
    if "LANGUAGE SKILLS:" in text:
        lang_section = text.split("LANGUAGE SKILLS:")[1].split('\n\n')[0]
        skills_l = [line.strip('- ').strip() for line in lang_section.split('\n') if line.strip()]
    
    if "SKILLS:" in text:
        skill_section = text.split("SKILLS:")[1].split('\n\n')[0]
        skills_ss = [line.strip('- ').strip() for line in skill_section.split('\n') if line.strip()]
    
    return {
        'name': name_parts[0] if len(name_parts) > 0 else "",
        'surname': name_parts[-1] if len(name_parts) > 1 else "",
        'phone': phones,
        'email': emails,
        'lives': address_line,
        'work': extract_work_experience(text),
        'dob': dob_match.group(1) if dob_match else "",
        'skills-l': skills_l,
        'skills-ss': skills_ss
    }

def extract_work_experience(text):
    if "WORK EXPERIENCE:" not in text:
        return []
    
    work_section = text.split("WORK EXPERIENCE:")[1].split('\n\n')[0]
    positions = []
    current_position = ""
    
    for line in work_section.split('\n'):
        line = line.strip()
        if line and not line.startswith('-'):
            if current_position:
                positions.append(current_position.strip())
            current_position = line
        elif line.startswith('-'):
            current_position += " " + line.strip('- ').strip()
    
    if current_position:
        positions.append(current_position.strip())
    
    return positions

def save_txt_results_to_json(data, json_filename):
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f