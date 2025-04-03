CREATE TABLE esercizio1.prod1v3 (
	prod_subcategory INT,
    prod_subcategory_id VARCHAR(255),
    prod_subcategory_desc VARCHAR(255),
    prod_category VARCHAR(255),
    prod_category_id FLOAT,
    prod_category_desc VARCHAR(255),
    prod_weight_class VARCHAR(50),
    prod_unit_of_measure VARCHAR(10),
    prod_pack_size VARCHAR(50),
    supplier_id VARCHAR(255),
    prod_status VARCHAR(50),
    prod_list_price FLOAT,
    prod_min_price FLOAT,
    prod_total VARCHAR(50),
    prod_total_id VARCHAR(255),
    prod_src_id VARCHAR(255),
    prod_eff_from VARCHAR(255),
    prod_eff_to VARCHAR(255),
    prod_valid CHAR(1),
    PRIMARY KEY (prod_subcategory)
);



LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/prod1v3.csv'  
INTO TABLE esercizio1.prod1v3  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(prod_subcategory,prod_subcategory_id,prod_subcategory_desc,prod_category,prod_category_id,prod_category_desc,prod_weight_class,prod_unit_of_measure,prod_pack_size,supplier_id,prod_status,prod_list_price,prod_min_price,prod_total,prod_total_id,prod_src_id,prod_eff_from,prod_eff_to,prod_valid);


ALTER TABLE `esercizio1`.`prod1v3` 
RENAME TO  `esercizio1`.`products` ;
