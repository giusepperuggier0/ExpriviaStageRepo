
# %%

import pandas as pd

# Importazione del dataset

df1 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/01_TB1_CProtetta2020.xls")


new_columns = [
    'Regione',
    'lunghezza_costa_km_2000',
    'costa_protetta_km_2000',
    'costa_protetta_percentuale_2000',
    'lunghezza_costa_km_2006',
    'costa_protetta_km_2006',
    'costa_protetta_percentuale_2006',
    'lunghezza_costa_km_2020',
    'costa_protetta_km_2020',
    'costa_protetta_percentuale_2020',
    'lunghezza_spiagge_km',
    'quota_spiaggia_percentuale',
    'lunghezza_spiagge_protette_km',
    'componente_spiagge_protette_percentuale',
    'costa_naturale_km',
    'costa_artificiale_km',
    'tratti_fittizi_km'
]

df1.columns = new_columns
df1 = df1.iloc[1:].reset_index(drop=True)

for col in df1.columns:
    if col != 'Regione':
        df1[col] = pd.to_numeric(df1[col], errors='coerce')

df1 = df1.drop(0, axis=0)

# Separa la riga dell'Italia dal resto dei dati
italia_row = df1[df1['Regione'] == 'ITALIA'].copy()
other_rows = df1[df1['Regione'] != 'ITALIA'].copy()


# Ordina prima per area geografica e poi per regione
other_rows = other_rows.sort_values(['Regione'])

# Aggiungi una colonna Area_Geografica anche alla riga Italia (opzionale)
italia_row['Area_Geografica'] = 'TOTALE'

# Concatena le regioni ordinate con la riga dell'Italia in fondo
df1 = pd.concat([other_rows, italia_row]).reset_index(drop=True)

# Fai partire l'indice da 1
df1.index = df1.index + 1

df1

# %%
import pandas as pd
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA'].copy()
 
# Calcoliamo la lunghezza totale della costa usando .loc[]
df1_filtered.loc[:, 'costa_totale_km'] = df1_filtered['costa_naturale_km'] + df1_filtered['costa_artificiale_km']
 
# Creazione della tabella
costa_completa = df1_filtered[['Regione', 'costa_naturale_km', 'costa_artificiale_km', 'costa_totale_km']]
print("Confronto tra costa naturale, costa artificiale e costa totale:")
costa_completa


# %%
import pandas as pd
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA'].copy()
 
import pandas as pd
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA'].copy()
 
# Calcoliamo le variazioni percentuali
df1_filtered['2000-2006'] = df1_filtered['costa_protetta_percentuale_2006'] - df1_filtered['costa_protetta_percentuale_2000']
df1_filtered['2006-2020'] = df1_filtered['costa_protetta_percentuale_2020'] - df1_filtered['costa_protetta_percentuale_2006']
df1_filtered['2000-2020'] = df1_filtered['costa_protetta_percentuale_2020'] - df1_filtered['costa_protetta_percentuale_2000']
 
# Creazione della tabella
costa_protetta_tabella = df1_filtered[['Regione', 'costa_protetta_percentuale_2000', 'costa_protetta_percentuale_2006', 'costa_protetta_percentuale_2020', '2000-2006', '2006-2020', '2000-2020']]
 
# Rinominiamo le colonne
costa_protetta_tabella = costa_protetta_tabella.rename(columns={
    'costa_protetta_percentuale_2000': 'costa_protetta_%_2000',
    'costa_protetta_percentuale_2006': 'costa_protetta_%_2006',
    'costa_protetta_percentuale_2020': 'costa_protetta_%_2020'
})
 
print("Distribuzione della percentuale di costa protetta e variazioni:")
costa_protetta_tabella

# %%
import matplotlib.pyplot as plt
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA']
 
# Dati per la creazione del grafico
regions = df1_filtered['Regione']
 
# Lunghezze delle coste per ciascun anno
length_2000 = df1_filtered['lunghezza_costa_km_2000']
length_2006 = df1_filtered['lunghezza_costa_km_2006']
length_2020 = df1_filtered['lunghezza_costa_km_2020']
 
# Creazione della figura
fig, ax = plt.subplots(figsize=(12, 6))
 
# Plotting dei dati
ax.plot(regions, length_2000, marker='o', linestyle='-', color='blue', label='2000')
ax.plot(regions, length_2006, marker='s', linestyle='--', color='green', label='2006')
ax.plot(regions, length_2020, marker='^', linestyle='-.', color='red', label='2020')
 
# Aggiunta di etichette e titolo
ax.set_xlabel('Regione')
ax.set_ylabel('Lunghezza delle coste (km)')
ax.set_title('Lunghezza delle coste per regione negli anni 2000, 2006 e 2020')
 
# Rotazione delle etichette dell'asse x per migliorare la leggibilità
plt.xticks(rotation=90)
 
# Aggiunta della legenda
ax.legend()
 
# Adattiamo il layout
plt.tight_layout()
plt.show()

#%%
import pandas as pd
import matplotlib.pyplot as plt
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA']
 
# Dati per la creazione del grafico
regions = df1_filtered['Regione']
costa_naturale = df1_filtered['costa_naturale_km']
costa_artificiale = df1_filtered['costa_artificiale_km']
lunghezza_totale = df1_filtered[['costa_naturale_km', 'costa_artificiale_km']].sum(axis=1)
 
# Creazione della figura
fig, ax = plt.subplots(figsize=(11, 8))
 
# Larghezza delle barre
bar_width = 0.3
 
# Posizioni delle barre sul grafico
r1 = range(len(regions))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
 
# Plotting dei dati
ax.bar(r1, lunghezza_totale, color='purple', width=bar_width, edgecolor='black', label='Lunghezza Totale')
ax.bar(r2, costa_naturale, color='pink', width=bar_width, edgecolor='black', label='Costa Naturale')
ax.bar(r3, costa_artificiale, color='brown', width=bar_width, edgecolor='black', label='Costa Artificiale')
 
# Aggiunta di etichette e titolo
ax.set_xlabel('Regione')
ax.set_ylabel('Lunghezza delle coste (km)')
ax.set_title('Confronto tra costa naturale, costa artificiale e lunghezza totale per regione', loc='center')
ax.set_xticks([r + bar_width for r in range(len(regions))])
ax.set_xticklabels(regions, rotation=90)
 
# Aggiunta della legenda
ax.legend()
 
# Adattiamo il layout
plt.tight_layout()
plt.show()
 
 
# %%
import pandas as pd
import matplotlib.pyplot as plt
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA']
 
# Calcoliamo le somme totali delle spiagge e delle spiagge protette
totale_spiagge = df1_filtered['lunghezza_spiagge_km'].sum()
totale_spiagge_protette = df1_filtered['lunghezza_spiagge_protette_km'].sum()
 
# Creiamo i dati per il grafico a torta
labels = ['Spiagge Protette', 'Spiagge Non Protette']
sizes = [totale_spiagge_protette, totale_spiagge - totale_spiagge_protette]
colors = ['green','#66b3ff']
 
# Creazione del grafico a torta
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.set_title('Distribuzione delle spiagge protette rispetto alla lunghezza totale delle spiagge')
 
# Adattiamo il layout
plt.tight_layout()
plt.show()
 
# %%
import pandas as pd
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA'].copy()
 
# Calcoliamo la lunghezza totale della costa usando .loc[]
df1_filtered.loc[:, 'costa_totale_km'] = df1_filtered['costa_naturale_km'] + df1_filtered['costa_artificiale_km']
 
# Creazione della tabella
costa_completa = df1_filtered[['Regione', 'costa_naturale_km', 'costa_artificiale_km', 'costa_totale_km']]
print("Confronto tra costa naturale, costa artificiale e costa totale:")
costa_completa
 
#%%
import pandas as pd
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA'].copy()
 
# Calcoliamo le somme totali delle spiagge e delle spiagge protette
totale_spiagge = df1_filtered['lunghezza_spiagge_km'].sum()
totale_spiagge_protette = df1_filtered['lunghezza_spiagge_protette_km'].sum()
percentuale_spiagge_protette = (totale_spiagge_protette / totale_spiagge) * 100
 
# Creazione della tabella
distribuzione_spiagge = {
    'Tipo di Spiaggia': ['Spiagge Protette', 'Spiagge Non Protette', 'Totale Spiagge'],
    'Lunghezza (km)': [totale_spiagge_protette, totale_spiagge - totale_spiagge_protette, totale_spiagge],
    'Percentuale (%)': [percentuale_spiagge_protette, 100 - percentuale_spiagge_protette, 100]
}
 
spiagge_protette_tabella = pd.DataFrame(distribuzione_spiagge)
print("Distribuzione delle spiagge protette rispetto alla lunghezza totale delle spiagge:")
spiagge_protette_tabella
 
# %%
import pandas as pd
 
# Rimuoviamo la riga "Italia" dal dataset
df1_filtered = df1[df1['Regione'] != 'ITALIA'].copy()
 
# Calcoliamo le variazioni in chilometri
df1_filtered['2000-2006'] = df1_filtered['costa_protetta_km_2006'] - df1_filtered['costa_protetta_km_2000']
df1_filtered['2006-2020'] = df1_filtered['costa_protetta_km_2020'] - df1_filtered['costa_protetta_km_2006']
df1_filtered['2000-2020'] = df1_filtered['costa_protetta_km_2020'] - df1_filtered['costa_protetta_km_2000']
 
# Creazione della tabella
costa_protetta_tabella = df1_filtered[['Regione', 'costa_protetta_km_2000', 'costa_protetta_km_2006', 'costa_protetta_km_2020', '2000-2006', '2006-2020', '2000-2020']]
 
# Rinominiamo le colonne
costa_protetta_tabella = costa_protetta_tabella.rename(columns={
    'costa_protetta_km_2000': 'Costa Protetta 2000 (km)',
    'costa_protetta_km_2006': 'Costa Protetta 2006 (km)',
    'costa_protetta_km_2020': 'Costa Protetta 2020 (km)',
    '2000-2006': '2000-2006 (km)',
    '2006-2020': '2006-2020 (km)',
    '2000-2020': '2000-2020 (km)'
})
 
print("Distribuzione della lunghezza della costa protetta e variazioni:")
costa_protetta_tabella




# %%
