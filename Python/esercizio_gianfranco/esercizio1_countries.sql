-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: esercizio1
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES (52769,'SG','Singapore','Asia',52793,'Asia',52802,'World total',52806,''),(52770,'IT','Italy','Western Europe',52799,'Europe',52803,'World total',52806,''),(52771,'CN','China','Asia',52793,'Asia',52802,'World total',52806,''),(52772,'CA','Canada','Northern America',52797,'Americas',52801,'World total',52806,''),(52773,'AR','Argentina','Southern America',52798,'Americas',52801,'World total',52806,''),(52774,'AU','Australia','Australia',52794,'Oceania',52805,'World total',52806,''),(52775,'BR','Brazil','Southern America',52798,'Americas',52801,'World total',52806,''),(52776,'DE','Germany','Western Europe',52799,'Europe',52803,'World total',52806,''),(52777,'DK','Denmark','Western Europe',52799,'Europe',52803,'World total',52806,''),(52778,'ES','Spain','Western Europe',52799,'Europe',52803,'World total',52806,''),(52779,'FR','France','Western Europe',52799,'Europe',52803,'World total',52806,''),(52780,'IE','Ireland','Western Europe',52799,'Europe',52803,'World total',52806,''),(52781,'IN','India','Asia',52793,'Asia',52802,'World total',52806,''),(52782,'JP','Japan','Asia',52793,'Asia',52802,'World total',52806,''),(52783,'MY','Malaysia','Asia',52793,'Asia',52802,'World total',52806,''),(52784,'NL','The Netherlands','Western Europe',52799,'Europe',52803,'World total',52806,''),(52785,'NZ','New Zealand','Australia',52794,'Oceania',52805,'World total',52806,''),(52786,'PL','Poland','Eastern Europe',52795,'Europe',52803,'World total',52806,''),(52787,'SA','Saudi Arabia','Middle East',52796,'Middle East',52804,'World total',52806,''),(52788,'TR','Turkey','Western Europe',52799,'Europe',52803,'World total',52806,''),(52789,'GB','United Kingdom','Western Europe',52799,'Europe',52803,'World total',52806,''),(52790,'US','United States of America','Northern America',52797,'Americas',52801,'World total',52806,''),(52791,'ZA','South Africa','Africa',52792,'Africa',52800,'World total',52806,'');
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-23 11:11:23
