CREATE TABLE channels (
    channel_id INTEGER PRIMARY KEY NOT NULL,
    channel_desc varchar(5000)(50),
    channel_class varchar(5000)(50),
    channel_class_id INTEGER,
    channel_total INTEGER,
    channel_total_id INTEGER
);

CREATE TABLE costs (
    prod_id INTEGER NOT NULL,
    time_id DATE NOT NULL,
    promo_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    unit_cost decimal(10,2),
    unit_amount decimal(10,2),
    PRIMARY KEY (prod_id, time_id, promo_id, channel_id)
);

CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY NOT NULL,
    country_iso_code varchar(5000)(200),
    country_name varchar(5000)(200),
    country_subregion varchar(5000)(200),
    country_subregion_id INTEGER,
    country_region varchar(5000)(200),
    country_region_id INTEGER,
    country_total varchar(5000)(200),
    country_total_id INTEGER,
    country_name_hist varchar(5000)(200)
);

CREATE TABLE customers (
    cust_id INTEGER NOT NULL PRIMARY KEY,
    cust_first_name varchar(5000)(255),
    cust_last_name varchar(5000)(255),
    cust_gender CHAR(1),
    cust_year_of_birth INTEGER,
    cust_marital_status varchar(5000)(50),
    cust_street_address varchar(5000)(255),
    cust_postal_code varchar(5000)(10),
    cust_city varchar(5000)(255),
    cust_city_id INTEGER,
    cust_state_province varchar(5000)(255),
    cust_state_province_id INTEGER,
    country_id INTEGER,
    cust_main_phone_decimal varchar(5000)(50),
    cust_income_level varchar(5000)(50),
    cust_credit_limit decimal(10,2),
    cust_email varchar(5000)(255),
    cust_total varchar(5000)(50),
    cust_total_id INTEGER,
    cust_src_id INTEGER,
    cust_eff_from DATE,
    cust_valid CHAR(1)
);

CREATE TABLE demographics (
    cust_id INTEGER NOT NULL PRIMARY KEY,
    education varchar(5000)(50),
    occupation varchar(5000)(50),
    household_size INTEGER,
    yrs_residence INTEGER,
    affinity_card CHAR(1),
    bulk_pack_diskettes CHAR(1),
    flat_panel_monitor CHAR(1),
    home_theater_package CHAR(1),
    bookkeeping_application CHAR(1),
    printer_supplies CHAR(1),
    y_box_games CHAR(1),
    os_doc_set_kanji CHAR(1),
    comments varchar(5000)
);

CREATE TABLE products (
    prod_subcategory_id INTEGER NOT NULL PRIMARY KEY,
    prod_subcategory varchar(5000)(255),
    prod_subcategory_desc varchar(5000)(255),
    prod_category varchar(5000)(255),
    prod_category_id decimal,
    prod_category_desc varchar(5000)(255),
    prod_weight_class varchar(5000)(50),
    prod_unit_of_measure varchar(5000)(10),
    prod_pack_size varchar(5000)(50),
    supplier_id varchar(5000)(255),
    prod_status varchar(5000)(50),
    prod_list_price decimal,
    prod_min_price decimal,
    prod_total varchar(5000)(50),
    prod_total_id varchar(5000)(255),
    prod_src_id varchar(5000)(255),
    prod_eff_from DATE,
    prod_eff_to DATE,
    prod_valid CHAR(1)
);

CREATE TABLE promo (
    promo_id INTEGER NOT NULL PRIMARY KEY,
    promo_name varchar(5000)(255),
    promo_subcategory varchar(5000)(255),
    promo_subcategory_id INTEGER,
    promo_category varchar(5000)(255),
    promo_category_id INTEGER,
    promo_cost decimal(10,2),
    promo_begin_date DATE,
    promo_end_date DATE,
    promo_total varchar(5000)(255),
    promo_total_id INTEGER
);

CREATE TABLE sales (
    prod_id INTEGER NOT NULL PRIMARY KEY,
    cust_id INTEGER NOT NULL PRIMARY KEY,
    time_id DATE NOT NULL PRIMARY KEY,
    channel_id INTEGER NOT NULL PRIMARY KEY,
    promo_id INTEGER NOT NULL PRIMARY KEY,
    quantity_sold INTEGER NOT NULL,
    amount_sold decimal(10,2) NOT NULL
);

CREATE TABLE time (
    time_id DATE NOT NULL PRIMARY KEY,
    day_name varchar(5000)(10) NOT NULL,
    day_decimal_in_week INTEGER NOT NULL,
    day_decimal_in_month INTEGER NOT NULL,
    calendar_week_decimal INTEGER NOT NULL,
    fiscal_week_decimal INTEGER NOT NULL,
    week_ending_day DATE NOT NULL,
    week_ending_day_id INTEGER NOT NULL,
    calendar_month_decimal INTEGER NOT NULL,
    fiscal_month_decimal INTEGER NOT NULL,
    calendar_month_desc varchar(5000)(50) NOT NULL,
    calendar_month_id INTEGER NOT NULL,
    fiscal_month_desc varchar(5000)(50) NOT NULL,
    fiscal_month_id INTEGER NOT NULL,
    days_in_cal_month INTEGER NOT NULL,
    days_in_fis_month INTEGER NOT NULL,
    end_of_cal_month DATE NOT NULL,
    end_of_fis_month DATE NOT NULL,
    calendar_month_name varchar(5000)(50) NOT NULL,
    fiscal_month_name varchar(5000)(50) NOT NULL,
    calendar_quarter_desc varchar(5000)(50) NOT NULL,
    calendar_quarter_id INTEGER NOT NULL,
    fiscal_quarter_desc varchar(5000)(50) NOT NULL,
    fiscal_quarter_id INTEGER NOT NULL,
    days_in_cal_quarter INTEGER NOT NULL,
    days_in_fis_quarter INTEGER NOT NULL,
    end_of_cal_quarter DATE NOT NULL,
    end_of_fis_quarter DATE NOT NULL,
    calendar_quarter_decimal INTEGER NOT NULL,
    fiscal_quarter_decimal INTEGER NOT NULL,
    calendar_year INTEGER NOT NULL,
    calendar_year_id INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_year_id INTEGER NOT NULL,
    days_in_cal_year INTEGER NOT NULL,
    days_in_fis_year INTEGER NOT NULL,
    end_of_cal_year DATE NOT NULL,
    end_of_fis_year DATE NOT NULL
);


ALTER TABLE new_schema.customers 
ADD CONSTRAINT fk_country_id
FOREIGN KEY (country_id) 
REFERENCES new_schema.countries (country_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION;

ALTER TABLE new_schema.sales 
ADD CONSTRAINT fk_cust_id
FOREIGN KEY (cust_id) 
REFERENCES new_schema.customers (cust_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION;

ALTER TABLE new_schema.products 
ADD CONSTRAINT fk_prod
FOREIGN KEY (prod_subcategory_id) 
REFERENCES new_schema.sales (prod_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION;

ALTER TABLE new_schema.costs 
ADD CONSTRAINT fk_channels_id
FOREIGN KEY (channel_id) 
REFERENCES new_schema.channels (channel_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION,
ADD CONSTRAINT fk_prod_id
FOREIGN KEY (prod_id) 
REFERENCES new_schema.products (prod_subcategory_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION,
ADD CONSTRAINT fk_promo_id
FOREIGN KEY (promo_id) 
REFERENCES new_schema.promo (promo_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION,
ADD CONSTRAINT fk_time_id
FOREIGN KEY (time_id) 
REFERENCES new_schema.time (time_id) 
ON DELETE NO ACTION 
ON UPDATE NO ACTION;

ALTER TABLE new_schema.demographics
ADD CONSTRAINT fk_cust_id
FOREIGN KEY (cust_id)
REFERENCES new_schema.customers (cust_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
