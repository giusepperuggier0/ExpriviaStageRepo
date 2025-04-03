import pandas as pd
import mysql.connector
import streamlit as st
import os

# Inizializzazione dello stato dell'applicazione
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'df_db' not in st.session_state:
    st.session_state.df_db = None
if 'table_exists' not in st.session_state:
    st.session_state.table_exists = False

# Configurazione della connessione al database MySQL
DB_CONFIG = {
    "host": "localhost",      
    "user": "root",           
    "password": "root",   
    "database": "progetto_dati" 
}

def create_connection(): #Crea una connessione al database MySQL
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        st.error(f"Errore di connessione al database: {str(e)}")
        return None

def check_table_exists(): #Verifica se la tabella dati esiste nel database
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'dati'")
        result = cursor.fetchone()
        return result is not None
        
    except Exception as e:
        st.error(f"Errore durante la verifica della tabella: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def create_table(df): #Crea una tabella nel database basata sulla struttura del DataFrame
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()

        # Controllo esistenza tabella
        if not check_table_exists():
            # Sanitizzazione nomi colonne
            columns = df.columns.tolist()
            columns_sanitized = [f"`{col.strip().replace(' ', '_').replace(',', '')}`" for col in columns]
            column_defs = ", ".join([f"{col} VARCHAR(255)" for col in columns_sanitized])
            create_table_query = f"CREATE TABLE dati (id INT AUTO_INCREMENT PRIMARY KEY, {column_defs})"
            
            cursor.execute(create_table_query)
            conn.commit()
            st.success("Tabella creata con successo!")
            st.session_state.table_exists = True
            return True
            
        return True
        
    except Exception as e:
        st.error(f"Errore nella creazione della tabella: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def is_table_empty(): #Verifica se la tabella dati è vuota
    try:
        conn = create_connection()
        if not conn:
            return True
            
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dati")
        count = cursor.fetchone()[0]
        return count == 0
    finally:
        if conn:
            conn.close()

def drop_table(): #Elimina completamente la tabella dal database
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # Disabilita temporaneamente i controlli delle chiavi esterne
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Elimina la tabella
        cursor.execute("DROP TABLE IF EXISTS dati")
        
        # Riabilita i controlli delle chiavi esterne
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        st.session_state.table_exists = False
        return True
        
    except Exception as e:
        st.error(f"Errore durante l'eliminazione della tabella: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def load_data_to_db(df):    #Carica i dati dal DataFrame al database
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()

        # Inserimento dei dati nella tabella
        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            insert_query = f"INSERT INTO dati ({', '.join(df.columns)}) VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        return True
        
    except Exception as e:
        st.error(f"Errore durante il caricamento dei dati: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def fetch_data_from_db():    #Recupera i dati dal database
    try:
        conn = create_connection()
        if not conn:
            return None
            
        return pd.read_sql("SELECT * FROM dati", conn)
        
    except Exception as e:
        st.error(f"Errore durante il recupero dei dati: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

# Interface Streamlit
st.title("Gestione Database CSV")

# Aggiorna lo stato della tabella
st.session_state.table_exists = check_table_exists()

# Caricamento del file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lettura del file CSV
        df = pd.read_csv(uploaded_file)
        
        # Creazione della tabella e caricamento dati
        if create_table(df) and is_table_empty():
            if load_data_to_db(df):
                st.session_state.file_uploaded = True
                st.success("Dati caricati con successo nel database!")
            else:
                st.error("Errore durante il caricamento dei dati")
        elif not is_table_empty():
            st.warning("I dati sono già stati caricati nel database!")
            
    except Exception as e:
        st.error(f"Errore durante la lettura del file CSV: {str(e)}")

# Pulsante per eliminare la tabella
if st.button("Elimina database"):
    if st.session_state.table_exists:
        # Chiedi conferma prima di procedere
        if st.warning("⚠️ Sei sicuro di voler eliminare completamente la tabella e tutti i suoi dati?"):
            if drop_table():
                # Reset dello stato dell'applicazione
                st.session_state.file_uploaded = False
                st.session_state.df_db = None
                st.session_state.table_exists = False
                st.success("Tabella eliminata con successo!")
                st.rerun()
    else:
        st.info("Non esiste alcuna tabella da eliminare.")

# Visualizzazione dei dati
if st.session_state.table_exists:
    st.write("### Dati nel Database")
    df_db = fetch_data_from_db()

    if df_db is not None and not df_db.empty:
        st.session_state.df_db = df_db
        st.dataframe(df_db)
        
        # Selezione colonne per il grafico
        columns = df_db.columns.tolist()[1:]  # Escludi la colonna ID
        col_x = st.selectbox("Scegli la colonna X", columns)
        col_y = st.selectbox("Scegli la colonna Y", columns)

        # Creazione del grafico
        if st.button("Genera Grafico"):
            st.bar_chart(df_db.set_index(col_x)[col_y])
    else:
        st.info("Nessun dato presente nella tabella.")
else:
    st.info("Nessuna tabella presente nel database. Carica un file CSV per iniziare.")