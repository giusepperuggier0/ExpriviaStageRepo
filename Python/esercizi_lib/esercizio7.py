print("Scrivi un programma che a partire da un elemento e una lista di elementi dica in output se l'elemento passato sia presente o meno nella lista.")

elements = ["ciao","mamma","guarda","come","mi","diverto"]

a = str(input("Inserisci un elemento e vediamo se la lista lo contiene!")).strip().lower()

if a in elements:
    index = elements.index(a)
    print(f"L'elemento \"{a}\" è nella lista all'indice {index}.")
else:
    print("L'elemento non è nella lista.")
