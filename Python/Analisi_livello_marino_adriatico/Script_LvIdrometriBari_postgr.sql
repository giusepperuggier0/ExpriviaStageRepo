CREATE TABLE dati_bari (
    id SERIAL primary KEY,
    ora TEXT,
    livello_idrometrico REAL,
    temperature REAL,
    press REAL
);

drop table dati_bari;

-- docker cp C:\Users\Giuseppe\Desktop\Stage_exprivia\Python\Analisi_livello_marino_adriatico\dati_bari.csv 8d250ffe000b:opt/dati_bari.csv

COPY dati_bari(id,ora, livello_idrometrico, temperature, press) 
FROM '/opt/dati_bari.csv' 
DELIMITER ',' CSV HEADER;
