#%%
import pandas as pd
from IPython.display import display

# Update the definition of the geographical areas
aree_geografiche = {
    'NORD': ['Veneto', 'Friuli-Venezia Giulia', 'Liguria', 'Emilia-Romagna'],
    'CENTRO': ['Toscana', 'Marche', 'Lazio'],
    'SUD': ['Abruzzo', 'Molise', 'Campania', 'Puglia', 'Basilicata', 'Calabria'],
    'ISOLE': ['Sicilia', 'Sardegna']
}

# Function to assign the geographical area
def assegna_area(regione):
    for area, regioni in aree_geografiche.items():
        if regione in regioni:
            return area
    return 'ALTRO'

# Import and initial preparation of the data
df2 = pd.read_excel("C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_coste/Difesa_costiera.xls")

df2.columns = df2.iloc[0]
df2 = df2.drop(0, axis=0)
df2.columns = df2.columns.str.strip()
df2['Regioni'] = df2['Regioni'].ffill()

# Create the pivot table
df_pivot = df2.pivot(index='Regioni', columns='Anno', 
                     values=['Isolotti', 'Opere Miste', 'Pennelli', 'Radenti', 'Scogliere', 'Totali'])

df_pivot.columns = [f"{col[0]}_{col[1]}" for col in df_pivot.columns]
df_pivot = df_pivot.reset_index()
df_pivot_cleaned = df_pivot.loc[:, ~df_pivot.columns.str.contains('nan')]
df2 = df_pivot_cleaned

italia_row = df2[df2['Regioni'].str.contains('Totale', case=False, na=False)]
other_rows = df2[~df2['Regioni'].str.contains('Totale', case=False, na=False)]

other_rows['Area_Geografica'] = other_rows['Regioni'].apply(assegna_area)

# Sorting and resetting the index
other_rows = other_rows.sort_values(['Area_Geografica', 'Regioni'])
df2 = pd.concat([other_rows, italia_row]).reset_index(drop=True) # Concatenate the dataframes and reset the index
df2.index = df2.index + 1

# Create separate dataframes for each area
df_nord = df2[df2['Area_Geografica'] == 'NORD']
df_centro = df2[df2['Area_Geografica'] == 'CENTRO']
df_sud = df2[df2['Area_Geografica'] == 'SUD']
df_isole = df2[df2['Area_Geografica'] == 'ISOLE']

# Display the dataframes
display(df_nord)
display(df_centro)
display(df_sud)
display(df_isole)

# %%
import matplotlib.pyplot as plt

def plot_bar_chart(df, ax, title):
    df_filtered = df.loc[:, ~df.columns.str.contains('Totali')]
    df_sum = df_filtered.iloc[:, 1:-1].sum() 
    df_sum.plot(kind='bar', ax=ax)
    ax.set_title(f'Difesa Costiera Aggregata - {title}')
    ax.set_xlabel('Tipi di Difesa Costiera')
    ax.set_ylabel('Valori Totali')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# Create a figure and axes
fig, axes = plt.subplots(1, 4, figsize=(20, 6))

# Plot bar charts for each area
plot_bar_chart(df_nord, axes[0], 'NORD')
plot_bar_chart(df_centro, axes[1], 'CENTRO')
plot_bar_chart(df_sud, axes[2], 'SUD')
plot_bar_chart(df_isole, axes[3], 'ISOLE')


plt.tight_layout()

plt.show()

# %%
import matplotlib.pyplot as plt

# Create a function to plot pie charts for specific years, excluding 'Totali' fields
def plot_pie_chart_year(df, year, ax, title):
    columns_of_year = [col for col in df.columns if str(year) in col and 'Totali' not in col]
    df_filtered = df.loc[:, columns_of_year]
    df_sum = df_filtered.sum()  # Sum the values for the specific year
    ax.pie(df_sum, labels=df_sum.index, autopct='%1.1f%%', startangle=140)
    ax.set_title(f'{title} - {year}')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Define the years of interest
years = [2000, 2006, 2020]

# Create a figure and axes
fig, axes = plt.subplots(len(years), 4, figsize=(20, 18))

# Plot pie charts for each area and each year
for i, year in enumerate(years):
    plot_pie_chart_year(df_nord, year, axes[i, 0], 'NORD')
    plot_pie_chart_year(df_centro, year, axes[i, 1], 'CENTRO')
    plot_pie_chart_year(df_sud, year, axes[i, 2], 'SUD')
    plot_pie_chart_year(df_isole, year, axes[i, 3], 'ISOLE')

# Adjust layout
plt.tight_layout()

# Show plots
plt.show()

