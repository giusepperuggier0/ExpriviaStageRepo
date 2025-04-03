# %%

#RIPARTIZIONE IN AREE GEOGRAFICHE
import pandas as pd

# Importazione e preparazione iniziale dei dati
df2 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/Difesa_costiera.xls")

df2.columns = df2.iloc[0]
df2 = df2.drop(0, axis=0)
df2.columns = df2.columns.str.strip()
df2['Regioni'] = df2['Regioni'].ffill()

# Creazione del pivot
df_pivot = df2.pivot(index='Regioni', columns='Anno', 
                     values=['Isolotti', 'Opere Miste', 'Pennelli', 'Radenti', 'Scogliere', 'Totali'])

df_pivot.columns = [f"{col[0]}_{col[1]}" for col in df_pivot.columns]
df_pivot = df_pivot.reset_index()
df_pivot_cleaned = df_pivot.loc[:, ~df_pivot.columns.str.contains('nan')]
df2 = df_pivot_cleaned

italia_row = df2[df2['Regioni'].str.contains('Totale', case=False, na=False)]
other_rows = df2[~df2['Regioni'].str.contains('Totale', case=False, na=False)]



other_rows = other_rows.sort_values(['Regioni'])


df2 = pd.concat([other_rows, italia_row]).reset_index(drop=True) # Unisci i dataframe e resetta l'indice


df2.index = df2.index + 1

df2


# %%
import pandas as pd
import matplotlib.pyplot as plt

# Selezione delle colonne di interesse
columns_of_interest = ['Totali_2000', 'Totali_2006', 'Totali_2020']

# Creazione del pivot

df_pivot_cleaned = df2.loc[:, ['Regioni'] + columns_of_interest]
italia_row = df_pivot_cleaned[df_pivot_cleaned['Regioni'].str.contains('Totale', case=False, na=False)]
other_rows = df_pivot_cleaned[~df_pivot_cleaned['Regioni'].str.contains('Totale', case=False, na=False)]

# Ordina e combina i dataframe
other_rows = other_rows.sort_values(['Regioni'])
df2 = pd.concat([other_rows, italia_row]).reset_index(drop=True)

# Aumenta l'indice di 1 per chiarezza
df2.index = df2.index + 1

# Plot dei dati
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df2['Regioni'], df2['Totali_2000'], label='Totale (km) 2000', marker='o')
ax.plot(df2['Regioni'], df2['Totali_2006'], label='Totale (km) 2006', marker='o')
ax.plot(df2['Regioni'], df2['Totali_2020'], label='Totale (km) 2020', marker='o')

ax.set_xlabel('Regioni')
ax.set_ylabel('Kilometri')
ax.set_title('Protezione Costiera in Italia')
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt

# Selezione delle colonne di interesse
columns_of_interest = ['Totali_2000', 'Totali_2006', 'Totali_2020']

# Creazione del pivot

df_pivot_cleaned = df2.loc[:, ['Regioni'] + columns_of_interest]
italia_row = df_pivot_cleaned[df_pivot_cleaned['Regioni'].str.contains('Totale', case=False, na=False)]
other_rows = df_pivot_cleaned[~df_pivot_cleaned['Regioni'].str.contains('Totale', case=False, na=False)]

# Ordina e combina i dataframe
other_rows = other_rows.sort_values(['Regioni'])
df2 = pd.concat([other_rows, italia_row]).reset_index(drop=True)

# Aumenta l'indice di 1 per chiarezza
df2.index = df2.index + 1

# Creazione degli istogrammi affiancati
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Istogramma per il 2000
axs[0].bar(df2['Regioni'], df2['Totali_2000'], color='b', alpha=0.7)
axs[0].set_xlabel('Regioni')
axs[0].set_ylabel('Kilometri')
axs[0].set_title('Totale Opere di Difesa Costiera nel 2000')
axs[0].tick_params(axis='x', rotation=90)

# Istogramma per il 2006
axs[1].bar(df2['Regioni'], df2['Totali_2006'], color='g', alpha=0.7)
axs[1].set_xlabel('Regioni')
axs[1].set_ylabel('Kilometri')
axs[1].set_title('Totale Opere di Difesa Costiera nel 2006')
axs[1].tick_params(axis='x', rotation=90)

# Istogramma per il 2020
axs[2].bar(df2['Regioni'], df2['Totali_2020'], color='r', alpha=0.7)
axs[2].set_xlabel('Regioni')
axs[2].set_ylabel('Kilometri')
axs[2].set_title('Totale Opere di Difesa Costiera nel 2020')
axs[2].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.show()

#%%

#RIPARTIZIONE IN AREE GEOGRAFICHE
import pandas as pd


# Importazione e preparazione iniziale dei dati
df2 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/Difesa_costiera.xls")

df2.columns = df2.iloc[0]
df2 = df2.drop(0, axis=0)
df2.columns = df2.columns.str.strip()
df2['Regioni'] = df2['Regioni'].ffill()

# Creazione del pivot
df_pivot = df2.pivot(index='Regioni', columns='Anno', 
                     values=['Isolotti', 'Opere Miste', 'Pennelli', 'Radenti', 'Scogliere', 'Totali'])

df_pivot.columns = [f"{col[0]}_{col[1]}" for col in df_pivot.columns]
df_pivot = df_pivot.reset_index()
df_pivot_cleaned = df_pivot.loc[:, ~df_pivot.columns.str.contains('nan')]
df2 = df_pivot_cleaned

italia_row = df2[df2['Regioni'].str.contains('Totale', case=False, na=False)]
other_rows = df2[~df2['Regioni'].str.contains('Totale', case=False, na=False)]



other_rows = other_rows.sort_values(['Regioni'])


df2 = pd.concat([other_rows, italia_row]).reset_index(drop=True) # Unisci i dataframe e resetta l'indice


df2.index = df2.index + 1

df2


# %%

#La regione con il numero massimo di interventi
import pandas as pd

# Calcola il totale degli interventi per ciascuna regione
df2['Totale_Interventi'] = df2[['Isolotti_2000', 'Isolotti_2006', 'Isolotti_2020',
                                'Opere Miste_2000', 'Opere Miste_2006', 'Opere Miste_2020',
                                'Pennelli_2000', 'Pennelli_2006', 'Pennelli_2020',
                                'Radenti_2000', 'Radenti_2006', 'Radenti_2020',
                                'Scogliere_2000', 'Scogliere_2006', 'Scogliere_2020']].sum(axis=1)

# Ordina le regioni per numero totale di interventi
df_sorted = df2.sort_values(by='Totale_Interventi', ascending=False)

# Stampa la tabella con i totali degli interventi
print(df_sorted[['Regioni', 'Totale_Interventi']])

# Determina la regione con il numero massimo di interventi
regione_massimo_interventi = df_sorted.iloc[0]

print("\nLa regione con il numero massimo di interventi è:", regione_massimo_interventi['Regioni'])
print("Numero totale di interventi:", regione_massimo_interventi['Totale_Interventi'])

# %%
import pandas as pd

# Calcola il totale degli interventi per ciascun anno
df2['Totale_2000'] = df2[['Isolotti_2000', 'Opere Miste_2000', 'Pennelli_2000', 'Radenti_2000', 'Scogliere_2000']].sum(axis=1)
df2['Totale_2006'] = df2[['Isolotti_2006', 'Opere Miste_2006', 'Pennelli_2006', 'Radenti_2006', 'Scogliere_2006']].sum(axis=1)
df2['Totale_2020'] = df2[['Isolotti_2020', 'Opere Miste_2020', 'Pennelli_2020', 'Radenti_2020', 'Scogliere_2020']].sum(axis=1)

# Determina la regione con il numero massimo di interventi per ciascun anno
regione_massimo_2000 = df2.loc[df2['Totale_2000'].idxmax()]
regione_massimo_2006 = df2.loc[df2['Totale_2006'].idxmax()]
regione_massimo_2020 = df2.loc[df2['Totale_2020'].idxmax()]

# Creazione della tabella
result = pd.DataFrame({
    'Anno': ['2000', '2006', '2020'],
    'Regione con max interventi': [regione_massimo_2000['Regioni'], regione_massimo_2006['Regioni'], regione_massimo_2020['Regioni']],
    'Numero totale di interventi': [regione_massimo_2000['Totale_2000'], regione_massimo_2006['Totale_2006'], regione_massimo_2020['Totale_2020']]
})

result


# %%
import pandas as pd

# Calcola il totale degli interventi per ciascun anno
df2['Totale_2000'] = df2[['Isolotti_2000', 'Opere Miste_2000', 'Pennelli_2000', 'Radenti_2000', 'Scogliere_2000']].sum(axis=1)
df2['Totale_2006'] = df2[['Isolotti_2006', 'Opere Miste_2006', 'Pennelli_2006', 'Radenti_2006', 'Scogliere_2006']].sum(axis=1)
df2['Totale_2020'] = df2[['Isolotti_2020', 'Opere Miste_2020', 'Pennelli_2020', 'Radenti_2020', 'Scogliere_2020']].sum(axis=1)

# Converte i totali in numerici
df2['Totale_2000'] = pd.to_numeric(df2['Totale_2000'], errors='coerce')
df2['Totale_2006'] = pd.to_numeric(df2['Totale_2006'], errors='coerce')
df2['Totale_2020'] = pd.to_numeric(df2['Totale_2020'], errors='coerce')

# Seleziona le prime 3 regioni con il maggior numero di interventi per ciascun anno
top_3_2000 = df2.nlargest(3, 'Totale_2000')[['Regioni', 'Totale_2000']]
top_3_2006 = df2.nlargest(3, 'Totale_2006')[['Regioni', 'Totale_2006']]
top_3_2020 = df2.nlargest(3, 'Totale_2020')[['Regioni', 'Totale_2020']]

# Creazione della tabella
result = pd.DataFrame({
    'Anno': ['2000'] * 3 + ['2006'] * 3 + ['2020'] * 3,
    'Regione': top_3_2000['Regioni'].tolist() + top_3_2006['Regioni'].tolist() + top_3_2020['Regioni'].tolist(),
    'Numero totale di interventi': top_3_2000['Totale_2000'].tolist() + top_3_2006['Totale_2006'].tolist() + top_3_2020['Totale_2020'].tolist()
})

print(result)

# %%
import pandas as pd


# Converte i dati in numerici
for col in ['Isolotti_2000', 'Isolotti_2006', 'Isolotti_2020', 'Opere Miste_2000', 'Opere Miste_2006', 'Opere Miste_2020',
            'Pennelli_2000', 'Pennelli_2006', 'Pennelli_2020', 'Radenti_2000', 'Radenti_2006', 'Radenti_2020',
            'Scogliere_2000', 'Scogliere_2006', 'Scogliere_2020']:
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

# Seleziona le prime 3 regioni con il maggior numero di interventi per ciascun tipo di opera e anno
top_3_isolotti_2000 = df2.nlargest(3, 'Isolotti_2000')[['Regioni', 'Isolotti_2000']]
top_3_isolotti_2006 = df2.nlargest(3, 'Isolotti_2006')[['Regioni', 'Isolotti_2006']]
top_3_isolotti_2020 = df2.nlargest(3, 'Isolotti_2020')[['Regioni', 'Isolotti_2020']]

top_3_opere_miste_2000 = df2.nlargest(3, 'Opere Miste_2000')[['Regioni', 'Opere Miste_2000']]
top_3_opere_miste_2006 = df2.nlargest(3, 'Opere Miste_2006')[['Regioni', 'Opere Miste_2006']]
top_3_opere_miste_2020 = df2.nlargest(3, 'Opere Miste_2020')[['Regioni', 'Opere Miste_2020']]

top_3_pennelli_2000 = df2.nlargest(3, 'Pennelli_2000')[['Regioni', 'Pennelli_2000']]
top_3_pennelli_2006 = df2.nlargest(3, 'Pennelli_2006')[['Regioni', 'Pennelli_2006']]
top_3_pennelli_2020 = df2.nlargest(3, 'Pennelli_2020')[['Regioni', 'Pennelli_2020']]

top_3_radenti_2000 = df2.nlargest(3, 'Radenti_2000')[['Regioni', 'Radenti_2000']]
top_3_radenti_2006 = df2.nlargest(3, 'Radenti_2006')[['Regioni', 'Radenti_2006']]
top_3_radenti_2020 = df2.nlargest(3, 'Radenti_2020')[['Regioni', 'Radenti_2020']]

top_3_scogliere_2000 = df2.nlargest(3, 'Scogliere_2000')[['Regioni', 'Scogliere_2000']]
top_3_scogliere_2006 = df2.nlargest(3, 'Scogliere_2006')[['Regioni', 'Scogliere_2006']]
top_3_scogliere_2020 = df2.nlargest(3, 'Scogliere_2020')[['Regioni', 'Scogliere_2020']]

# Creazione delle tabelle
table_2000 = pd.DataFrame({
    'Regione Isolotti': top_3_isolotti_2000['Regioni'].tolist(),
    'Numero Isolotti': top_3_isolotti_2000['Isolotti_2000'].tolist(),
    'Regione Opere Miste': top_3_opere_miste_2000['Regioni'].tolist(),
    'Numero Opere Miste': top_3_opere_miste_2000['Opere Miste_2000'].tolist(),
    'Regione Pennelli': top_3_pennelli_2000['Regioni'].tolist(),
    'Numero Pennelli': top_3_pennelli_2000['Pennelli_2000'].tolist(),
    'Regione Radenti': top_3_radenti_2000['Regioni'].tolist(),
    'Numero Radenti': top_3_radenti_2000['Radenti_2000'].tolist(),
    'Regione Scogliere': top_3_scogliere_2000['Regioni'].tolist(),
    'Numero Scogliere': top_3_scogliere_2000['Scogliere_2000'].tolist(),
})

table_2006 = pd.DataFrame({
    'Regione Isolotti': top_3_isolotti_2006['Regioni'].tolist(),
    'Numero Isolotti': top_3_isolotti_2006['Isolotti_2006'].tolist(),
    'Regione Opere Miste': top_3_opere_miste_2006['Regioni'].tolist(),
    'Numero Opere Miste': top_3_opere_miste_2006['Opere Miste_2006'].tolist(),
    'Regione Pennelli': top_3_pennelli_2006['Regioni'].tolist(),
    'Numero Pennelli': top_3_pennelli_2006['Pennelli_2006'].tolist(),
    'Regione Radenti': top_3_radenti_2006['Regioni'].tolist(),
    'Numero Radenti': top_3_radenti_2006['Radenti_2006'].tolist(),
    'Regione Scogliere': top_3_scogliere_2006['Regioni'].tolist(),
    'Numero Scogliere': top_3_scogliere_2006['Scogliere_2006'].tolist(),
})

table_2020 = pd.DataFrame({
    'Regione Isolotti': top_3_isolotti_2020['Regioni'].tolist(),
    'Numero Isolotti': top_3_isolotti_2020['Isolotti_2020'].tolist(),
    'Regione Opere Miste': top_3_opere_miste_2020['Regioni'].tolist(),
    'Numero Opere Miste': top_3_opere_miste_2020['Opere Miste_2020'].tolist(),
    'Regione Pennelli': top_3_pennelli_2020['Regioni'].tolist(),
    'Numero Pennelli': top_3_pennelli_2020['Pennelli_2020'].tolist(),
    'Regione Radenti': top_3_radenti_2020['Regioni'].tolist(),
    'Numero Radenti': top_3_radenti_2020['Radenti_2020'].tolist(),
    'Regione Scogliere': top_3_scogliere_2020['Regioni'].tolist(),
    'Numero Scogliere': top_3_scogliere_2020['Scogliere_2020'].tolist(),
})


table_2000

table_2006

table_2020

# %%
import pandas as pd
import matplotlib.pyplot as plt

# Importazione e preparazione iniziale dei dati
df2 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/Difesa_costiera.xls")

df2.columns = df2.iloc[0]
df2 = df2.drop(0, axis=0)
df2.columns = df2.columns.str.strip()
df2['Regioni'] = df2['Regioni'].ffill()

# Creazione del pivot
df_pivot = df2.pivot(index='Regioni', columns='Anno', 
                     values=['Isolotti', 'Opere Miste', 'Pennelli', 'Radenti', 'Scogliere', 'Totali'])

df_pivot.columns = [f"{col[0]}_{col[1]}" for col in df_pivot.columns]
df_pivot = df_pivot.reset_index()
df_pivot_cleaned = df_pivot.loc[:, ~df_pivot.columns.str.contains('nan')]
df2 = df_pivot_cleaned

italia_row = df2[df2['Regioni'].str.contains('Totale', case=False, na=False)]
other_rows = df2[~df2['Regioni'].str.contains('Totale', case=False, na=False)]

other_rows = other_rows.sort_values(['Regioni'])

df2 = pd.concat([other_rows, italia_row]).reset_index(drop=True)  # Unisci i dataframe e resetta l'indice

df2.index = df2.index + 1

# Continua con il resto del codice
# Somma delle opere rigide di difesa costiera per ciascun anno
somme_2000 = df2[['Isolotti_2000', 'Opere Miste_2000', 'Pennelli_2000', 'Radenti_2000', 'Scogliere_2000']].sum()
somme_2006 = df2[['Isolotti_2006', 'Opere Miste_2006', 'Pennelli_2006', 'Radenti_2006', 'Scogliere_2006']].sum()
somme_2020 = df2[['Isolotti_2020', 'Opere Miste_2020', 'Pennelli_2020', 'Radenti_2020', 'Scogliere_2020']].sum()

# Creazione dei grafici a torta senza etichette e con legenda
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Funzione per creare grafici a torta senza etichette
def pie_chart(ax, sizes, colors):
    ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.set_aspect('equal')

# Impostazione dei colori
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
labels = ['Isolotti', 'Opere Miste', 'Pennelli', 'Radenti', 'Scogliere']

# Grafico a torta per il 2000
axes[0].text(0.5, 1.1, '2000', horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes, fontsize=12, fontweight='bold')
pie_chart(axes[0], somme_2000, colors)

# Grafico a torta per il 2006
axes[1].text(0.5, 1.1, '2006', horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes, fontsize=12, fontweight='bold')
pie_chart(axes[1], somme_2006, colors)

# Grafico a torta per il 2020
axes[2].text(0.5, 1.1, '2020', horizontalalignment='center', verticalalignment='center', transform=axes[2].transAxes, fontsize=12, fontweight='bold')
pie_chart(axes[2], somme_2020, colors)

# Unico titolo sopra tutti i grafici
fig.suptitle('Distribuzione Opere Rigide di Difesa Costiera', fontsize=16, fontweight='bold')

# Aggiunta della legenda
fig.legend(labels, loc='upper right', bbox_to_anchor=(1, 1))

# Adattiamo il layout
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

 




# %%
