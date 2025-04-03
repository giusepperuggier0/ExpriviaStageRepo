import re
import pdfplumber

pdf_path = "C:\\Users\\Giuseppe\\Desktop\\Stage_exprivia\\Python\\Pdf_extr\\Curriculum_pdf\\CVSaraPaolazzo_en.pdf"

with pdfplumber.open(pdf_path) as pdf:
    pages = pdf.pages[0]
    texts = pages.extract_text()
    print(texts)


def estrai_info(testo):
    dati = {}

    
    match_nome = re.search(r"Curriculum Vitae\s+([A-Za-z ]+)", testo)
    if match_nome:
        dati["Nome_Cognome"] = match_nome.group(1).strip()

   
    match_indirizzo = re.search(r"(\d{1,5}[-\s]?[A-Za-z\s]+,\s?[A-Za-z\s]+,\s?[A-Za-z\s]+,\s?\d{2,5}[-\s]?\d{0,5},\s?[A-Za-z\s]+)", testo)
    if match_indirizzo:
        dati["Indirizzo"] = match_indirizzo.group(1).strip()

    
    match_email = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", testo)
    if match_email:
        dati["Email"] = match_email.group(0).strip()

    
    phone_numbers = re.findall(r'\+\d+', texts.replace(" ", ""))
    if phone_numbers:
        dati["Telefono"] = ", ".join(phone_numbers)

    
    match_dob = re.search(r"Date of birth (\d{2}/\d{2}/\d{4})", testo)
    if match_dob:
        dati["Data di Nascita"] = match_dob.group(1).strip()

    return dati


info_cv = estrai_info(texts)


print(info_cv)
