print("Buongiorno! Inserisci una lista di numeri e scopri il maggiore.")

numbers = []  

while True:
    try:
        a = int(input("Inserisci un numero: "))
        numbers.append(a)
    except ValueError:
        print("Per favore, inserisci un numero valido.")
        continue

    risposta = input("Vuoi inserire un altro numero? S/N: ").strip().upper()
    if risposta == "N":
        break
    elif risposta != "S":
        print("Risposta non valida, ma presumo tu voglia continuare.")
        continue

if numbers: 
    print(f"Il numero maggiore inserito è: {max(numbers)}")
else:
    print("Non hai inserito alcun numero.")
