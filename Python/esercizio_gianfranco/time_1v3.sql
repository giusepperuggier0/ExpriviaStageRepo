CREATE TABLE esercizio1.time_v3 (
    time_id DATETIME NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_number_in_week INT NOT NULL,
    day_number_in_month INT NOT NULL,
    calendar_week_number INT NOT NULL,
    fiscal_week_number INT NOT NULL,
    week_ending_day DATETIME NOT NULL,
    week_ending_day_id INT NOT NULL,
    calendar_month_number INT NOT NULL,
    fiscal_month_number INT NOT NULL,
    calendar_month_desc VARCHAR(50) NOT NULL,
    calendar_month_id INT NOT NULL,
    fiscal_month_desc VARCHAR(50) NOT NULL,
    fiscal_month_id INT NOT NULL,
    days_in_cal_month INT NOT NULL,
    days_in_fis_month INT NOT NULL,
    end_of_cal_month DATETIME NOT NULL,
    end_of_fis_month DATETIME NOT NULL,
    calendar_month_name VARCHAR(50) NOT NULL,
    fiscal_month_name VARCHAR(50) NOT NULL,
    calendar_quarter_desc VARCHAR(50) NOT NULL,
    calendar_quarter_id INT NOT NULL,
    fiscal_quarter_desc VARCHAR(50) NOT NULL,
    fiscal_quarter_id INT NOT NULL,
    days_in_cal_quarter INT NOT NULL,
    days_in_fis_quarter INT NOT NULL,
    end_of_cal_quarter DATETIME NOT NULL,
    end_of_fis_quarter DATETIME NOT NULL,
    calendar_quarter_number INT NOT NULL,
    fiscal_quarter_number INT NOT NULL,
    calendar_year INT NOT NULL,
    calendar_year_id INT NOT NULL,
    fiscal_year INT NOT NULL,
    fiscal_year_id INT NOT NULL,
    days_in_cal_year INT NOT NULL,
    days_in_fis_year INT NOT NULL,
    end_of_cal_year DATETIME NOT NULL,
    end_of_fis_year DATETIME NOT NULL,
    PRIMARY KEY (time_id)
);


LOAD DATA LOCAL INFILE 'C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/esercizio_gianfranco/time_1v3.csv'  
INTO TABLE esercizio1.time_1v3  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'  
IGNORE 1 ROWS  
(time_id,day_name,day_number_in_week,day_number_in_month,calendar_week_number,fiscal_week_number,week_ending_day,week_ending_day_id,calendar_month_number,fiscal_month_number,calendar_month_desc,calendar_month_id,fiscal_month_desc,fiscal_month_id,days_in_cal_month,days_in_fis_month,end_of_cal_month,end_of_fis_month,calendar_month_name,fiscal_month_name,calendar_quarter_desc,calendar_quarter_id,fiscal_quarter_desc,fiscal_quarter_id,days_in_cal_quarter,days_in_fis_quarter,end_of_cal_quarter,end_of_fis_quarter,calendar_quarter_number,fiscal_quarter_number,calendar_year,calendar_year_id,fiscal_year,fiscal_year_id,days_in_cal_year,days_in_fis_year,end_of_cal_year,end_of_fis_year);


ALTER TABLE `esercizio1`.`time1v3` 
RENAME TO  `esercizio1`.`time` ;
