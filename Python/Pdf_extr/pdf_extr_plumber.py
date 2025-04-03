from pdf2image import convert_from_path
import pytesseract

pdf_path = "101311384_europass.pdf"

images = convert_from_path(pdf_path)  
text = pytesseract.image_to_string(images[0], lang="eng")  # Cambia 'eng' con 'ita' per italiano

print(text)
