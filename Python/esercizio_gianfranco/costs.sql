CREATE TABLE esercizio1.costs (
    prod_id INT NOT NULL,
    time_id DATE NOT NULL,
    promo_id INT NOT NULL,
    channel_id INT NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (prod_id, time_id, promo_id, channel_id)
);




LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/costs.csv'  
INTO TABLE esercizio1.costs  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(prod_id,time_id,promo_id,channel_id,unit_cost,unit_price);

ALTER TABLE `esercizio1`.`costs` 
RENAME TO  `esercizio1`.`costs` ;


ALTER TABLE esercizio1.costs 
ADD CONSTRAINT `fk_time`
FOREIGN KEY (`time_id`) 
REFERENCES esercizio1.time (`time_id`) 
ON DELETE NO ACTION ON UPDATE NO ACTION;

sqldeveloper data model