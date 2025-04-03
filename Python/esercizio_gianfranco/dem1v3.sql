CREATE TABLE esercizio1.dem1v3 (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,  -- ID cliente, generato automaticamente
    education VARCHAR(50),                   -- Livello di istruzione (es. Masters, Bach., HS-grad)
    occupation VARCHAR(50),                   -- Professione (es. Prof., Sales, Cleric.)
    household_size INT,                        -- Dimensione del nucleo familiare
    yrs_residence INT,                         -- Anni di residenza
    affinity_card BOOLEAN,                     -- Carta fedeltà (1 = Sì, 0 = No)
    bulk_pack_diskettes BOOLEAN,               -- Acquisto dischetti (1 = Sì, 0 = No)
    flat_panel_monitor BOOLEAN,                -- Acquisto monitor (1 = Sì, 0 = No)
    home_theater_package BOOLEAN,              -- Acquisto home theater (1 = Sì, 0 = No)
    bookkeeping_application BOOLEAN,           -- Acquisto software contabilità (1 = Sì, 0 = No)
    printer_supplies BOOLEAN,                  -- Acquisto forniture per stampante (1 = Sì, 0 = No)
    y_box_games BOOLEAN,                       -- Acquisto giochi Y-Box (1 = Sì, 0 = No)
    os_doc_set_kanji BOOLEAN,                  -- Acquisto documentazione OS Kanji (1 = Sì, 0 = No)
    comments TEXT                              -- Commenti del cliente
);




LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/dem1v3.csv'  
INTO TABLE esercizio1.dem1v3  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(education, occupation, household_size, yrs_residence, affinity_card,  
bulk_pack_diskettes, flat_panel_monitor, home_theater_package, bookkeeping_application,  
printer_supplies, y_box_games, os_doc_set_kanji, comments);


 
 ALTER TABLE esercizio1.demographics 
ADD CONSTRAINT `fk_cust_ID`
  FOREIGN KEY (`cust_id`)
  REFERENCES esercizio1.customers (`cust_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;