CREATE TABLE esercizio1.sale1v3 (
    prod_id INT NOT NULL,
    cust_id INT NOT NULL,
    time_id DATE NOT NULL,
    channel_id INT NOT NULL,
    promo_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    amount_sold DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (prod_id, cust_id, time_id, channel_id, promo_id)
);



LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/sale1v3.csv'  
INTO TABLE esercizio1.sale1v3  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(prod_id,cust_id,time_id,channel_id,promo_id,quantity_sold,amount_sold);

ALTER TABLE esercizio1.sales
ADD CONSTRAINT `fk_prod_id`
FOREIGN KEY (`prod_id`) 
REFERENCES esercizio1.products (`prod_id`) 
ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE esercizio1.sales
ADD CONSTRAINT `fk_cust_id`
FOREIGN KEY (`cust_id`) 
REFERENCES esercizio1.customers (`cust_id`) 
ON DELETE NO ACTION ON UPDATE NO ACTION;