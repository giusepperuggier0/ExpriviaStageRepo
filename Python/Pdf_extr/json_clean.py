import json
import re
from spacy.training.iob_utils import offsets_to_biluo_tags

def clean_and_realign_annotations(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            data = json.loads(line)
            text = data["text"]
            
            # Normalizza il testo mantenendo la struttura delle sezioni
            cleaned_text = re.sub(r'(\S)\n(\S)', r'\1 \2', text)  # Sostituisce solo newline tra parole
            cleaned_text = re.sub(r'\n+', '\n', cleaned_text)  # Mantiene singoli newline come separatori
            
            # Ricalcola gli offset per le annotazioni
            new_annotations = []
            for start, end, label in data["label"]:
                entity_text = text[start:end]
                
                # Cerca l'entità nel testo pulito con flessibilità
                search_pattern = re.escape(entity_text.replace('\n', ' ').strip())
                match = re.search(search_pattern, cleaned_text)
                
                if match:
                    new_start, new_end = match.span()
                    new_annotations.append([new_start, new_end, label])
                else:
                    # Prova una ricerca più flessibile per le esperienze lavorative
                    if label == "work":
                        simplified_entity = entity_text.split('\n')[0].strip()  # Prende solo la prima riga
                        match = re.search(re.escape(simplified_entity), cleaned_text)
                        if match:
                            new_start, new_end = match.span()
                            new_annotations.append([new_start, new_end, label])
                            continue
                    
                    print(f"Entità non trovata: '{entity_text[:50]}...' nel testo: '{cleaned_text[:50]}...'")
            
            # Salva il dato corretto
            new_data = {
                "id": data["id"],
                "text": cleaned_text,
                "label": new_annotations,
                "Comments": data.get("Comments", [])
            }
            outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')

# Percorsi dei file
clean_and_realign_annotations("C:/Users/Giuseppe/Downloads/json_train_data/admin.jsonl", "C:/Users/Giuseppe/Downloads/json_train_data/admin_corrected.jsonl")