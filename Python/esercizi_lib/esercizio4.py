print("Buongiorno hai la possibilità di inserire una lettera e capire se hai inserito una vocale oppure no")

a = str(input("Inserisci il carattere: ")).lower()

if a in "aeiou":
    print("il carattere inserito è una vocale")
else:
    print("Il carattere inserito non è una vocale")