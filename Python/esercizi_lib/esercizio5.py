print("Buongiorno inserisci una lista di numeri e tiriamo fuori la somma!")
sum = 0
numbers =[]
while True:
    a = int(input("Inserisci un numero: "))
    numbers.append(a)
    sum += a
    risposta = str(input("Vuoi inserire un nuovo numero ? S/N ")).upper()
    if risposta == "S":
        continue
    else:
        print("La lista di numeri è " + str(numbers))
        print("La somma è " +str(sum))
        break


