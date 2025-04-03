-- docker cp 'C:\Users\Giuseppe\Desktop\Stage_exprivia\Python\Analisi_livello_marino_adriatico\dati_bari.csv' e91138ed3160:/opt/hive/bin/


CREATE TABLE dati_bari (
    id INT,
    ora STRING,
    livello_idrometrico FLOAT,
    temp FLOAT,
    press FLOAT
) ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH 'dati_bari.csv' INTO TABLE dati_bari;


SELECT * from dati_bari db ;