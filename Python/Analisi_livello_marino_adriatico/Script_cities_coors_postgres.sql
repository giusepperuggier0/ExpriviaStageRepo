CREATE TABLE cities_coord (
    id SERIAL PRIMARY KEY,
    citta TEXT,
    h24 REAL,
    h48 REAL,
    h72 REAL,
    lng DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    mare TEXT
);

-- docker cp C:\Users\Giuseppe\Desktop\Stage_exprivia\Python\Analisi_livello_marino_adriatico\cities_coord.csv 8d250ffe000b:opt/cities_coord.csv

COPY cities_coord(id,citta, h24, h48, h72, lng, lat, mare) 
FROM '/opt/cities_coord.csv' 
DELIMITER ',' CSV HEADER;