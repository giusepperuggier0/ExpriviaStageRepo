import pandas as pd

# Leggi il file .dat (specificando il delimitatore se necessario, ad esempio '\t' per tabulazione o ',' per virgola)
df = pd.read_csv('C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/dem1v3.dat', delimiter='|',
                  engine='python')

# Salva il DataFrame in un file CSV
df.to_csv('C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/dem1v3.csv',index=False)

print("File CSV creato con successo!")