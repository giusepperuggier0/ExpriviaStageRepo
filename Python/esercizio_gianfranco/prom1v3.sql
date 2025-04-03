CREATE TABLE esercizio1.prom1v3 (
    promo_id INT PRIMARY KEY,
    promo_name VARCHAR(255) NOT NULL,
    promo_subcategory VARCHAR(255) NOT NULL,
    promo_subcategory_id INT NOT NULL,
    promo_category VARCHAR(255) NOT NULL,
    promo_category_id INT NOT NULL,
    promo_cost DECIMAL(10,2) NOT NULL,
    promo_begin_date DATETIME NOT NULL,
    promo_end_date DATETIME NOT NULL,
    promo_total VARCHAR(100) NOT NULL,
    promo_total_id INT NOT NULL
);


LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/prom1v3.csv'  
INTO TABLE esercizio1.prom1v3  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(promo_id,promo_name,promo_subcategory,promo_subcategory_id,promo_category,promo_category_id,promo_cost,promo_begin_date,promo_end_date,promo_total,promo_total_id);


ALTER TABLE `esercizio1`.`cust1v3` 
RENAME TO  `esercizio1`.`customers` ;
