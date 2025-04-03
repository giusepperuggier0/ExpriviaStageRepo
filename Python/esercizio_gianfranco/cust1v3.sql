CREATE TABLE cust1v3 (
    cust_id INT NOT NULL,
    cust_first_name VARCHAR(50) NOT NULL,
    cust_last_name VARCHAR(50) NOT NULL,
    cust_gender CHAR(1) NOT NULL,
    cust_year_of_birth INT NOT NULL,
    cust_marital_status VARCHAR(20),
    cust_street_address VARCHAR(100),
    cust_postal_code VARCHAR(20),
    cust_city VARCHAR(50),
    cust_city_id INT,
    cust_state_province VARCHAR(50),
    cust_state_province_id INT,
    country_id INT NOT NULL,
    cust_main_phone_number VARCHAR(20),
    cust_income_level VARCHAR(50),
    cust_credit_limit DECIMAL(10,2),
    cust_email VARCHAR(100),
    cust_total VARCHAR(50),
    cust_total_id INT,
    cust_src_id INT,
    cust_eff_from DATETIME,
    cust_eff_to DATETIME,
    cust_valid CHAR(1),
    PRIMARY KEY (cust_id)
);

LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/cust1v3.csv'  
INTO TABLE esercizio1.cust1v3  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(cust_id,cust_first_name,cust_last_name,cust_gender,cust_year_of_birth,cust_marital_status,cust_street_address,cust_postal_code,cust_city,cust_city_id,cust_state_province,cust_state_province_id,country_id,cust_main_phone_number,cust_income_level,cust_credit_limit,cust_email,cust_total,cust_total_id,cust_src_id,cust_eff_from,cust_eff_to,cust_valid);


ALTER TABLE esercizio1.`customers` 
ADD CONSTRAINT `fk_country_id`
  FOREIGN KEY (`country_id`)
  REFERENCES esercizio1.`countries` (`country_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
 

 