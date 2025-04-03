print("Buongiorno hai la possibilità di inserire tre numeri e capire qual'è il maggiore")

a = int(input("Inserisci il primo numero: "))
b = int(input("Inserisci il secondo numero: "))
c = int(input("Inserisci il terzo numero: "))

if a > b and a > c:
    print("Il maggiore è " + str(a))
elif b > c and b > a:
    print("Il maggiore è " + str(b))
else:
    print("Il maggiore è " + str(c))