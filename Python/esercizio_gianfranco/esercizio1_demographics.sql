CREATE TABLE `demographics` (
  `cust_id` int NOT NULL AUTO_INCREMENT,
  `education` varchar(50) DEFAULT NULL,
  `occupation` varchar(50) DEFAULT NULL,
  `household_size` int DEFAULT NULL,
  `yrs_residence` int DEFAULT NULL,
  `affinity_card` tinyint(1) DEFAULT NULL,
  `bulk_pack_diskettes` tinyint(1) DEFAULT NULL,
  `flat_panel_monitor` tinyint(1) DEFAULT NULL,
  `home_theater_package` tinyint(1) DEFAULT NULL,
  `bookkeeping_application` tinyint(1) DEFAULT NULL,
  `printer_supplies` tinyint(1) DEFAULT NULL,
  `y_box_games` tinyint(1) DEFAULT NULL,
  `os_doc_set_kanji` tinyint(1) DEFAULT NULL,
  `comments` text,
  PRIMARY KEY (`cust_id`),
  CONSTRAINT `fk_cust_ID` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`cust_id`)
);


CREATE TABLE `products` (
  `prod_subcategory_id` int NOT NULL,
  `prod_subcategory` varchar(255) DEFAULT NULL,
  `prod_subcategory_desc` varchar(255) DEFAULT NULL,
  `prod_category` varchar(255) DEFAULT NULL,
  `prod_category_id` float DEFAULT NULL,
  `prod_category_desc` varchar(255) DEFAULT NULL,
  `prod_weight_class` varchar(50) DEFAULT NULL,
  `prod_unit_of_measure` varchar(10) DEFAULT NULL,
  `prod_pack_size` varchar(50) DEFAULT NULL,
  `supplier_id` varchar(255) DEFAULT NULL,
  `prod_status` varchar(50) DEFAULT NULL,
  `prod_list_price` float DEFAULT NULL,
  `prod_min_price` float DEFAULT NULL,
  `prod_total` varchar(50) DEFAULT NULL,
  `prod_total_id` varchar(255) DEFAULT NULL,
  `prod_src_id` varchar(255) DEFAULT NULL,
  `prod_eff_from` varchar(255) DEFAULT NULL,
  `prod_eff_to` varchar(255) DEFAULT NULL,
  `prod_valid` char(1) DEFAULT NULL,
  KEY `fk_prod_idx` (`prod_subcategory_id`),
  CONSTRAINT `fk_prod` FOREIGN KEY (`prod_subcategory_id`) REFERENCES `sales` (`prod_id`)
);

CREATE TABLE `promo` (
  `promo_id` int NOT NULL,
  `promo_name` varchar(255) NOT NULL,
  `promo_subcategory` varchar(255) NOT NULL,
  `promo_subcategory_id` int NOT NULL,
  `promo_category` varchar(255) NOT NULL,
  `promo_category_id` int NOT NULL,
  `promo_cost` decimal(10,2) NOT NULL,
  `promo_begin_date` date NOT NULL,
  `promo_end_date` date NOT NULL,
  `promo_total` varchar(100) NOT NULL,
  `promo_total_id` int NOT NULL,
  PRIMARY KEY (`promo_id`)
);

CREATE TABLE `sales` (
  `prod_id` int NOT NULL,
  `cust_id` int NOT NULL,
  `time_id` date NOT NULL,
  `channel_id` int NOT NULL,
  `promo_id` int NOT NULL,
  `quantity_sold` int NOT NULL,
  `amount_sold` decimal(10,2) NOT NULL,
  PRIMARY KEY (`prod_id`,`cust_id`,`time_id`,`channel_id`,`promo_id`),
  KEY `cust_id` (`cust_id`),
  CONSTRAINT `fk_cust` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`cust_id`)
);

CREATE TABLE `time` (
  `time_id` date NOT NULL,
  `day_name` varchar(10) NOT NULL,
  `day_number_in_week` int NOT NULL,
  `day_number_in_month` int NOT NULL,
  `calendar_week_number` int NOT NULL,
  `fiscal_week_number` int NOT NULL,
  `week_ending_day` date NOT NULL,
  `week_ending_day_id` int NOT NULL,
  `calendar_month_number` int NOT NULL,
  `fiscal_month_number` int NOT NULL,
  `calendar_month_desc` varchar(50) NOT NULL,
  `calendar_month_id` int NOT NULL,
  `fiscal_month_desc` varchar(50) NOT NULL,
  `fiscal_month_id` int NOT NULL,
  `days_in_cal_month` int NOT NULL,
  `days_in_fis_month` int NOT NULL,
  `end_of_cal_month` date NOT NULL,
  `end_of_fis_month` date NOT NULL,
  `calendar_month_name` varchar(50) NOT NULL,
  `fiscal_month_name` varchar(50) NOT NULL,
  `calendar_quarter_desc` varchar(50) NOT NULL,
  `calendar_quarter_id` int NOT NULL,
  `fiscal_quarter_desc` varchar(50) NOT NULL,
  `fiscal_quarter_id` int NOT NULL,
  `days_in_cal_quarter` int NOT NULL,
  `days_in_fis_quarter` int NOT NULL,
  `end_of_cal_quarter` date NOT NULL,
  `end_of_fis_quarter` date NOT NULL,
  `calendar_quarter_number` int NOT NULL,
  `fiscal_quarter_number` int NOT NULL,
  `calendar_year` int NOT NULL,
  `calendar_year_id` int NOT NULL,
  `fiscal_year` int NOT NULL,
  `fiscal_year_id` int NOT NULL,
  `days_in_cal_year` int NOT NULL,
  `days_in_fis_year` int NOT NULL,
  `end_of_cal_year` date NOT NULL,
  `end_of_fis_year` date NOT NULL,
  PRIMARY KEY (`time_id`)
);

CREATE TABLE `customers` (
  `cust_id` int NOT NULL,
  `cust_first_name` varchar(50) NOT NULL,
  `cust_last_name` varchar(50) NOT NULL,
  `cust_gender` char(1) NOT NULL,
  `cust_year_of_birth` int NOT NULL,
  `cust_marital_status` varchar(20) DEFAULT NULL,
  `cust_street_address` varchar(100) DEFAULT NULL,
  `cust_postal_code` varchar(20) DEFAULT NULL,
  `cust_city` varchar(50) DEFAULT NULL,
  `cust_city_id` int DEFAULT NULL,
  `cust_state_province` varchar(50) DEFAULT NULL,
  `cust_state_province_id` int DEFAULT NULL,
  `country_id` int NOT NULL,
  `cust_main_phone_number` varchar(20) DEFAULT NULL,
  `cust_income_level` varchar(50) DEFAULT NULL,
  `cust_credit_limit` decimal(10,2) DEFAULT NULL,
  `cust_email` varchar(100) DEFAULT NULL,
  `cust_total` varchar(50) DEFAULT NULL,
  `cust_total_id` int DEFAULT NULL,
  `cust_src_id` int DEFAULT NULL,
  `cust_eff_from` date DEFAULT NULL,
  `cust_valid` char(1) DEFAULT NULL,
  PRIMARY KEY (`cust_id`),
  KEY `country_id_idx` (`country_id`),
  CONSTRAINT `fk_country_id` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`)
);

CREATE TABLE `countries` (
  `country_id` int NOT NULL,
  `country_iso_code` varchar(20) DEFAULT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `country_subregion` varchar(20) DEFAULT NULL,
  `country_subregion_id` int DEFAULT NULL,
  `country_region` varchar(20) DEFAULT NULL,
  `country_region_id` int DEFAULT NULL,
  `country_total` varchar(20) DEFAULT NULL,
  `country_total_id` int DEFAULT NULL,
  `country_name_hist` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`country_id`)
);

CREATE TABLE `costs` (
  `prod_id` int NOT NULL,
  `time_id` date NOT NULL,
  `promo_id` int NOT NULL,
  `channel_id` int NOT NULL,
  `unit_cost` decimal(10,2) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`prod_id`,`time_id`,`promo_id`,`channel_id`),
  KEY `fk_promo_idx` (`promo_id`),
  KEY `fk_channels_idx` (`channel_id`),
  KEY `fk_time` (`time_id`),
  CONSTRAINT `fk_channels` FOREIGN KEY (`channel_id`) REFERENCES `channels` (`channel_id`),
  CONSTRAINT `fk_prod_id` FOREIGN KEY (`prod_id`) REFERENCES `products` (`prod_subcategory_id`),
  CONSTRAINT `fk_promo` FOREIGN KEY (`promo_id`) REFERENCES `promo` (`promo_id`),
  CONSTRAINT `fk_time` FOREIGN KEY (`time_id`) REFERENCES `time` (`time_id`)
);

CREATE TABLE `channels` (
  `channel_id` int NOT NULL,
  `channel_desc` varchar(50) NOT NULL,
  `channel_class` varchar(20) NOT NULL,
  `channel_class_id` int NOT NULL,
  `channel_total` varchar(20) NOT NULL,
  `channel_total_id` int NOT NULL,
  PRIMARY KEY (`channel_id`),
  KEY `idx_channel_class` (`channel_class`),
  KEY `idx_channel_class_id` (`channel_class_id`)
);