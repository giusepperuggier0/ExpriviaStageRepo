import re
import pdfplumber
import spacy 
import pandas as pd 
from spacy import displacy

pdf_path = "C:\\Users\\Giuseppe\\Desktop\\Stage_exprivia\\Python\\Pdf_extr\\Curriculum_pdf\\cv_somot_europass_en_nov2017.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]  
    texts = page.extract_text()
    #print(texts)

nlp = spacy.load("en_core_web_trf")  
doc = nlp(texts)

entities = [(ent.text, ent.label_) for ent in doc.ents]
df = pd.DataFrame(entities, columns=['text', 'type'])
print(df.head(30))

def extract_info(df):
    #Person
    name = df[df['type'] == 'PERSON'].iloc[0]['text']
    
    # Indirizzo
    address  = df[df['type'] == 'GPE'].iloc[0]['text']

    # Email
    emails = [word for word in texts.split() if '@' in word]
    
    # Estrazione dell'esperienza lavorativa
    work_entries = re.findall(r'([^\n]*?(present|current|now|today)[^\n]*)\n', texts, re.IGNORECASE)
    current_work = [entry[0].strip() for entry in work_entries]
    if not current_work:
        current_work = ["Esperienza non trovata"]
    
    # Estrazione della data di nascita
    dob_entries = df[df['type'].str.upper() == 'DATE']['text'].values
    date_of_birth = ""
    if len(dob_entries) > 0:
        date_match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', dob_entries[0])
        if date_match:
            date_of_birth = date_match.group()
        else:
            date_of_birth = dob_entries[0]  

    # Estrazione dei numeri di telefono
    phone_numbers = re.findall(r'\+\d+', texts.replace(" ", ""))

    return {
        'name': name,
        'address': address,
        'emails': emails,
        'phone_numbers': phone_numbers,
        'date_of_birth': date_of_birth,
        'experience': current_work
    }

info = extract_info(df)

print("\n---- Informazioni ----")
print("Nome Cognome:", info['name'])
print("Città di Residenza:", info['address'])
print("Emails:", info['emails'])
print("Data di nascita:", info['date_of_birth'])
print("Numeri di telefono:", ", ".join(info['phone_numbers'])) 
print("Esperienza attuale:", info['experience'])
