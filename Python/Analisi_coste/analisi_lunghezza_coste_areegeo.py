#%%
import pandas as pd
from IPython.display import display

# Importazione del dataset
df1 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/01_TB1_CProtetta2020.xls")

# Definizione delle ripartizioni geografiche
aree_geografiche = {
    'NORD': ['Veneto', 'Friuli-Venezia Giulia', 'Liguria', 'Emilia-Romagna'],
    'CENTRO': ['Toscana', 'Marche', 'Lazio'],
    'SUD': ['Abruzzo', 'Molise', 'Campania', 'Puglia', 'Basilicata', 'Calabria'],
    'ISOLE': ['Sicilia', 'Sardegna']
}

# Funzione per assegnare l'area geografica
def assegna_area(regione):
    for area, regioni in aree_geografiche.items():
        if regione in regioni:
            return area
    return 'ALTRO'  # per gestire eventuali regioni non mappate

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

# Aggiungi la colonna dell'area geografica
other_rows['Area_Geografica'] = other_rows['Regione'].apply(assegna_area)

# Ordina prima per area geografica e poi per regione
other_rows = other_rows.sort_values(['Area_Geografica', 'Regione'])

# Escludi la riga "TOTALE"
other_rows = other_rows[other_rows['Area_Geografica'] != 'TOTALE']

# Fai partire l'indice da 1
other_rows.index = other_rows.index + 1

# Crea i DataFrame separati per ogni area geografica
df_nord = other_rows[other_rows['Area_Geografica'] == 'NORD']
df_centro = other_rows[other_rows['Area_Geografica'] == 'CENTRO']
df_sud = other_rows[other_rows['Area_Geografica'] == 'SUD']
df_isole = other_rows[other_rows['Area_Geografica'] == 'ISOLE']

# Visualizza i DataFrame
display(df_nord)
display(df_centro)
display(df_sud)
display(df_isole)

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Importiamo numpy per gestire gli array numerici

# Importazione del dataset
df1 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/01_TB1_CProtetta2020.xls")

# Definizione delle ripartizioni geografiche
aree_geografiche = {
    'NORD': ['Veneto', 'Friuli-Venezia Giulia', 'Liguria', 'Emilia-Romagna'],
    'CENTRO': ['Toscana', 'Marche', 'Lazio'],
    'SUD': ['Abruzzo', 'Molise', 'Campania', 'Puglia', 'Basilicata', 'Calabria'],
    'ISOLE': ['Sicilia', 'Sardegna']
}

# Funzione per assegnare l'area geografica
def assegna_area(regione):
    for area, regioni in aree_geografiche.items():
        if regione in regioni:
            return area
    return 'ALTRO'  # Per gestire eventuali regioni non mappate

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

# Aggiungi la colonna dell'area geografica
other_rows['Area_Geografica'] = other_rows['Regione'].apply(assegna_area)

# Ordina prima per area geografica e poi per regione
other_rows = other_rows.sort_values(['Area_Geografica', 'Regione'])

# Escludi la riga "TOTALE"
other_rows = other_rows[other_rows['Area_Geografica'] != 'TOTALE']

# Crea un DataFrame aggregato per le aree geografiche e gli anni
df_agg = other_rows.groupby('Area_Geografica').sum()

# Creiamo un array numerico per le aree geografiche
x = np.arange(len(df_agg.index))  # Indici numerici per le aree geografiche

# Plot del grafico a barre
fig, ax = plt.subplots(figsize=(14, 7))

years = ['2000', '2006', '2020']
colors = ['yellow', 'orange', 'red']
width = 0.15  # Larghezza di ogni barra


for i, year in enumerate(years):
    ax.bar(
        x + i * width,  # Utilizziamo l'array numerico invece di una stringa
        df_agg[f'lunghezza_costa_km_{year}'],
        width=width,
        label=f'Lunghezza delle coste nel {year}',
        color=colors[i],
        edgecolor='black'
    )

# Etichette e titolo
ax.set_xlabel('Aree Geografiche')
ax.set_ylabel('Lunghezza delle Coste (km)')
ax.set_title('Lunghezza delle Coste per Aree Geografiche e Anni')
ax.set_xticks(x + width)  # Posizioniamo le etichette delle aree geografiche
ax.set_xticklabels(df_agg.index)  # Assegniamo i nomi delle aree geografiche
ax.legend()

plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt
 
# Creazione delle figure e degli assi
fig, axs = plt.subplots(2, 2, figsize=(12, 12))
 
# DataFrame Nord
df_nord_filtered = df_nord[df_nord['Regione'] != 'ITALIA']
totale_spiagge_nord = df_nord_filtered['lunghezza_spiagge_km'].sum()
totale_spiagge_protette_nord = df_nord_filtered['lunghezza_spiagge_protette_km'].sum()
sizes_nord = [totale_spiagge_protette_nord, totale_spiagge_nord - totale_spiagge_protette_nord]
labels = ['Spiagge Protette', 'Spiagge Non Protette']
colors = ['green', '#66b3ff']
axs[0, 0].pie(sizes_nord, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
axs[0, 0].set_title('Nord')
 
# DataFrame Centro
df_centro_filtered = df_centro[df_centro['Regione'] != 'ITALIA']
totale_spiagge_centro = df_centro_filtered['lunghezza_spiagge_km'].sum()
totale_spiagge_protette_centro = df_centro_filtered['lunghezza_spiagge_protette_km'].sum()
sizes_centro = [totale_spiagge_protette_centro, totale_spiagge_centro - totale_spiagge_protette_centro]
axs[0, 1].pie(sizes_centro, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
axs[0, 1].set_title('Centro')
 
# DataFrame Sud
df_sud_filtered = df_sud[df_sud['Regione'] != 'ITALIA']
totale_spiagge_sud = df_sud_filtered['lunghezza_spiagge_km'].sum()
totale_spiagge_protette_sud = df_sud_filtered['lunghezza_spiagge_protette_km'].sum()
sizes_sud = [totale_spiagge_protette_sud, totale_spiagge_sud - totale_spiagge_protette_sud]
axs[1, 0].pie(sizes_sud, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
axs[1, 0].set_title('Sud')
 
# DataFrame Isole
df_isole_filtered = df_isole[df_isole['Regione'] != 'ITALIA']
totale_spiagge_isole = df_isole_filtered['lunghezza_spiagge_km'].sum()
totale_spiagge_protette_isole = df_isole_filtered['lunghezza_spiagge_protette_km'].sum()
sizes_isole = [totale_spiagge_protette_isole, totale_spiagge_isole - totale_spiagge_protette_isole]
axs[1, 1].pie(sizes_isole, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
axs[1, 1].set_title('Isole')
 
# Adattiamo il layout
plt.suptitle('Distribuzione delle spiagge protette per area geografica')
plt.tight_layout()
plt.show()

# %%
import pandas as pd
import matplotlib.pyplot as plt

# Definizione delle ripartizioni geografiche
aree_geografiche = {
    'NORD': ['Veneto', 'Friuli-Venezia Giulia', 'Liguria', 'Emilia-Romagna'],
    'CENTRO': ['Toscana', 'Marche', 'Lazio'],
    'SUD': ['Abruzzo', 'Molise', 'Campania', 'Puglia', 'Basilicata', 'Calabria'],
    'ISOLE': ['Sicilia', 'Sardegna']
}

# Funzione per assegnare l'area geografica
def assegna_area(regione):
    for area, regioni in aree_geografiche.items():
        if regione in regioni:
            return area


# Importazione del dataset
df1 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/01_TB1_CProtetta2020.xls")

# Rinominiamo le colonne
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

# Convertiamo le colonne numeriche
for col in df1.columns:
    if col != 'Regione':
        df1[col] = pd.to_numeric(df1[col], errors='coerce')

# **Aggiungiamo la colonna Area_Geografica**
df1['Area_Geografica'] = df1['Regione'].apply(assegna_area)

# **Ora possiamo filtrare correttamente**
df1_filtered = df1[df1['Regione'] != 'ITALIA']

# Raggruppiamo i dati per area geografica
km_2000 = df1_filtered.groupby('Area_Geografica')['costa_protetta_km_2000'].sum()
km_2006 = df1_filtered.groupby('Area_Geografica')['costa_protetta_km_2006'].sum()
km_2020 = df1_filtered.groupby('Area_Geografica')['costa_protetta_km_2020'].sum()

# Lista delle aree geografiche ordinate
Area_Geografica = km_2000.index

# Creazione della figura e degli assi per i sottoplot
fig, ax = plt.subplots(figsize=(10, 6))

# Larghezza delle barre
bar_width = 0.2

# Posizioni delle barre sul grafico
r1 = range(len(Area_Geografica))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Plotting dei dati
ax.bar(r1, km_2000, color='brown', width=bar_width, edgecolor='black', label='2000')
ax.bar(r2, km_2006, color='orange', width=bar_width, edgecolor='black', label='2006')
ax.bar(r3, km_2020, color='yellow', width=bar_width, edgecolor='black', label='2020')

# Aggiunta di etichette e titolo
ax.set_xlabel('Area Geografica')
ax.set_ylabel('Lunghezza della costa protetta (km)')
ax.set_title('Variazione della lunghezza della costa protetta tra il 2000, 2006 e 2020')
ax.set_xticks([r + bar_width for r in range(len(Area_Geografica))])
ax.set_xticklabels(Area_Geografica, rotation=0)

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

# Raggruppiamo i dati per Area Geografica
grouped_data = df1_filtered.groupby('Area_Geografica')[['costa_naturale_km', 'costa_artificiale_km']].sum()

# Estrarre i dati correttamente
Area_Geografica = grouped_data.index  # Ora ha la stessa forma delle altre serie
costa_naturale = grouped_data['costa_naturale_km']
costa_artificiale = grouped_data['costa_artificiale_km']
lunghezza_totale = costa_naturale + costa_artificiale

# Creazione della figura
fig, ax = plt.subplots(figsize=(9, 7))

# Larghezza delle barre
bar_width = 0.3

# Posizioni delle barre sul grafico
r1 = range(len(Area_Geografica))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Plotting dei dati
ax.bar(r1, lunghezza_totale, color='purple', width=bar_width, edgecolor='black', label='Lunghezza Totale')
ax.bar(r2, costa_naturale, color='pink', width=bar_width, edgecolor='black', label='Costa Naturale')
ax.bar(r3, costa_artificiale, color='brown', width=bar_width, edgecolor='black', label='Costa Artificiale')

# Aggiunta di etichette e titolo
ax.set_xlabel('Area Geografica')
ax.set_ylabel('Lunghezza delle coste (km)')
ax.set_title('Confronto tra costa naturale, costa artificiale e lunghezza totale per area geografica', loc='center')
ax.set_xticks([r + bar_width for r in range(len(Area_Geografica))])
ax.set_xticklabels(Area_Geografica, rotation=0)

# Aggiunta della legenda
ax.legend()

# Adattiamo il layout
plt.tight_layout()
plt.show()

 
# %%
