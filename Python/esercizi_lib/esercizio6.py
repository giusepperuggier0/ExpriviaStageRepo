print("Buongiorno inserisci una lista di numeri e tiriamo fuori la moltiplicazione!")
mult = 1
numbers =[]
while True:
    a = int(input("Inserisci un numero: "))
    numbers.append(a)
    mult *= a
    risposta = str(input("Vuoi inserire un nuovo numero ? S/N ")).upper()
    if risposta == "S":
        continue
    else:
        print("La lista di numeri è " + str(numbers))
        print("La moltiplicazione è " +str(mult))
        break


