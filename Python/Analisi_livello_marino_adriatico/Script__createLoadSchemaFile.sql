-- docker cp 'C:\Users\Giuseppe\Desktop\Stage_exprivia\Python\Analisi_livello_marino\Medie_Ultimi3GG.csv' e91138ed3160:/opt/hive/bin/
-- copia il file da locale in hive e poi con il comando sotto LOAD DATA LOCAL lo copia da hive alla tabella

Create TABLE coste(
	ID INT,
	CITTA String,
	24H Float,
	48H Float,
	72H Float
)ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");


LOAD DATA LOCAL INPATH 'Medie_Ultimi3GG.csv' INTO TABLE coste;

select * from coste c ;

Create TABLE coste_areaGeo(
	ID INT,
	CITTA String,
	AREA_GEOGRAFICA String,
	24H Float,
	48H Float,
	72H Float
)ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");

-- docker cp 'C:\Users\Giuseppe\Desktop\Stage_exprivia\Python\Analisi_livello_marino\Medie_Ultimi3GG_AreaGeo.csv' e91138ed3160:/opt/hive/bin/
-- copia il file da locale in hive e poi con il comando sotto LOAD DATA LOCAL lo copia da hive alla tabella

LOAD DATA LOCAL INPATH 'Medie_Ultimi3GG_AreaGeo.csv' INTO TABLE coste_areageo;

select * from coste_areageo;

