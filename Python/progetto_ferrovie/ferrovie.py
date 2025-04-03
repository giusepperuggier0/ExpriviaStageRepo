
import pandas as pd
import matplotlib.pyplot as plt 
import streamlit as st 
st.title("Caricamento e Visualizzazione dei Dati")

# Caricamento file
uploaded_file = st.file_uploader("Carica un file CSV o Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Leggere il file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("### Anteprima dei Dati")
        st.dataframe(df)

        # Selezione della colonna per la visualizzazione
        columns = df.columns.tolist()
        col_x = st.selectbox("Scegli la colonna X", columns)
        col_y = st.selectbox("Scegli la colonna Y", columns)

        # Creazione grafico
        if st.button("Genera Grafico"):
            fig, ax = plt.subplots()
            df.plot(kind="bar", x=col_x, y=col_y, ax=ax)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")
