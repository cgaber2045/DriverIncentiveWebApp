-- MySQL dump 10.13  Distrib 5.7.32, for Linux (x86_64)
--
-- Host: cpsc4910.crxd6v3fbudk.us-east-1.rds.amazonaws.com    Database: website
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
-- SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

-- SET @@GLOBAL.GTID_PURGED='';

--
-- Table structure for table `Product_Orders`
--

DROP TABLE IF EXISTS `Product_Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Product_Orders` (
  `Driver_ID` int NOT NULL,
  `TimeStamp` datetime NOT NULL,
  `rating` int DEFAULT NULL,
  `Product_ID` int DEFAULT NULL,
  `Sponsor_ID` int DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Order_ID` int DEFAULT NULL,
  `canceled` tinyint(1) NOT NULL,
  KEY `Driver_ID` (`Driver_ID`),
  KEY `Product_ID` (`Product_ID`),
  CONSTRAINT `Product_Orders_ibfk_1` FOREIGN KEY (`Driver_ID`) REFERENCES `driver` (`driver_id`),
  CONSTRAINT `Product_Orders_ibfk_2` FOREIGN KEY (`Product_ID`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product_Orders`
--

LOCK TABLES `Product_Orders` WRITE;
/*!40000 ALTER TABLE `Product_Orders` DISABLE KEYS */;
INSERT INTO `Product_Orders` VALUES (17,'2020-11-10 01:56:52',NULL,17,3,0.00,NULL,0),(17,'2020-11-10 01:58:36',NULL,14,3,0.00,NULL,0),(17,'2020-11-12 21:41:10',3,17,NULL,0.00,NULL,0),(17,'2020-11-12 21:45:07',3,17,NULL,0.00,NULL,0),(17,'2020-11-12 22:33:19',5,17,NULL,0.00,NULL,0),(17,'2020-11-17 21:23:13',3,18,1,950.00,8,1),(17,'2020-11-17 21:33:07',3,31,1,1699.00,9,1),(17,'2020-11-17 21:37:29',3,26,1,358.00,10,0),(17,'2020-11-17 21:37:30',3,30,1,650.00,10,0),(17,'2020-11-19 17:26:30',3,26,1,358.00,11,0),(17,'2020-11-19 17:30:33',3,26,1,358.00,12,0),(17,'2020-11-19 17:44:05',3,17,3,3.00,13,0),(17,'2020-11-19 17:52:07',3,30,1,650.00,14,1),(17,'2020-11-19 23:01:35',3,17,3,3.00,17,1),(17,'2020-11-19 18:14:27',3,18,1,950.00,18,0),(17,'2020-11-19 19:35:34',3,26,1,358.00,19,1),(17,'2020-11-19 19:40:49',3,26,1,358.00,20,1),(17,'2020-11-19 19:41:09',3,30,1,650.00,21,1),(17,'2020-11-19 20:49:05',3,26,1,358.00,22,1),(17,'2020-11-23 12:43:11',3,30,1,650.00,23,1),(17,'2020-11-23 12:44:59',3,26,1,358.00,24,1),(17,'2020-11-23 12:47:18',3,26,1,358.00,25,1),(17,'2020-11-23 12:49:40',3,26,1,358.00,26,1),(17,'2020-11-23 12:57:54',3,26,1,358.00,27,0),(17,'2020-11-23 13:01:07',3,30,1,650.00,28,0),(17,'2020-11-23 18:04:06',3,26,1,358.00,29,0),(17,'2020-11-23 18:27:32',3,36,2,25.00,30,0),(17,'2020-11-23 18:27:32',3,38,2,7.00,30,0),(17,'2020-11-24 20:59:56',3,26,1,358.00,31,0),(17,'2020-11-24 15:59:56',3,26,1,358.00,31,0),(17,'2020-11-24 20:59:56',3,26,1,358.00,31,0),(10,'2020-11-25 18:56:11',3,17,3,3.00,32,1),(10,'2020-11-25 19:21:27',3,14,3,0.00,33,1),(10,'2020-11-25 19:27:12',3,17,3,3.00,17,1),(17,'2020-11-28 20:28:30',3,32,1,4.00,34,0),(17,'2020-11-28 20:30:07',3,26,1,358.00,35,0),(17,'2020-11-28 20:31:04',3,51,1,26.00,36,0),(17,'2020-11-28 20:35:11',3,32,1,4.00,37,0),(17,'2020-11-28 20:36:39',3,26,1,358.00,38,0);
/*!40000 ALTER TABLE `Product_Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `first_name` varchar(20) DEFAULT NULL,
  `mid_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `admin_id` int NOT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `pwd` varchar(255) DEFAULT NULL,
  `date_join` date DEFAULT NULL,
  `date_leave` date DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('Will','NULL','Sherrer','will',2,'NULL','wsherrer16@gmail.com','sha256$ReIlhpuN$4ba825045c7934f2b42e122aafea3fae4812d24d596cf82a0719b7b0ff3936ac','2020-10-15','0000-00-00',1),('Chris','E','Gaber','cgaber',3,'NULL','NULL','sha256$C8KGSaPY$98cacffc24850ea264d50291013f401546b75e6e51a05cef43ada63f16137c4c','2020-10-19','0000-00-00',1),('NULL','NULL','NULL','testad',4,'NULL','NULL','sha256$1C7K0fJ8$26bbc86a0ad6af84f5a58981a28e6ac7d3971ca6c85be31ecff342962d1934d7','2020-11-02','0000-00-00',1),('System','NULL','','System',5,'NULL','NULL','sha256$kLJ1ahaq$c4b68e9c57291a455bfa98d5e0298380fa367c5bda7d27f43e7719b18a905135','2020-11-06','0000-00-00',1),('Evan','R','Hastings','evan',6,'8005882300','evan@example.com','sha256$Yp5RLcJH$f22192ad54c5edd38e65db56292e3828923a23efa0afdad9a2e31d8b3e46164e','2020-11-07','0000-00-00',1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `driver` (
  `first_name` varchar(20) DEFAULT NULL,
  `mid_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `driver_id` int NOT NULL,
  `address` varchar(40) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `pwd` varchar(255) DEFAULT NULL,
  `date_join` date DEFAULT NULL,
  `date_leave` date DEFAULT NULL,
  `image` longblob,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`driver_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES ('Evan','Robert','Hastings','evanrh',1,'123 Example St','8005882300','evan@something.net','sha256$F4vZRuqS$3231c16f1d2bcad5703c0a655843d6397eec0be82e5a584c47efbcd3cc0ee303','2020-10-08','0000-00-00',NULL,1),('Evan','NULL','Hastings','erhasti',10,'123 Easy St','123123123','e@e.com','sha256$1LkrKrjz$173d4e1d785a2c85dd20f028884d0192f0ff9fea949e4bd3480398398f23223e','2020-10-12','0000-00-00',NULL,1),('Christopher','NULL','Robin','crobin',11,'123 Pooh St','1231231231','crobin@disney.com','sha256$PCE1PuRf$cc680b08ed4aa911edfc3edd952201d17125445634dae5137dc67e3396452faa','2020-10-14','0000-00-00',NULL,1),('David','d','Gleaton','David',14,'1234','5616516515','d@example.com','sha256$QJ5IXgWh$55411b9ad9ce1efa8c34ef977b0502885c8e5a5a21388a42f7224c6377e57a21','0000-00-00','2020-10-14',_binary 'NULL',1),('Will','NULL','Driver','wsherre',15,'NULL','NULL','NULL','sha256$ZnemmC24$fb7447e507b1c0476b7f203187a4aac5d6d553566c4049df4806730d1cb163ca','2020-10-19','0000-00-00',_binary 'NULL',1),('Test','NULL','Driver','testdrive',17,'NULL','NULL','NULL','sha256$YvFbi8uo$56b003a250d805498930b5a009dcbef483e5a266d6d19bcb27e195b37a4127f6','2020-10-21','0000-00-00',_binary 'NULL',1),('app','NULL','test','app_test',25,'theest','8888888888','s@s.com','sha256$DIeTJC6H$31c28aab8058d252ce453b1c6eb70ac3b75bb2eb7723f05339f1ddb23419818d','2020-11-11','0000-00-00',_binary 'NULL',1),('Ima','NULL','Cow','imacow',26,'123 Lonely Rd','1231231231','icow@clemson.edu','sha256$fqr3HjBu$914b503f6c6ad29ec0b6dabf9a723eb38729720a6929a2b97fdaa2edae398d61','2020-11-25','0000-00-00',_binary 'NULL',1),('NULL','NULL','NULL','jack',27,'NULL','NULL','NULL','sha256$4FkTM1Pl$4ed8bb6c7e4a4224d2c1cc253d674d034877deba1f4474d345f0131a57f6c571','2020-11-25','0000-00-00',_binary 'NULL',1);
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driver_bridge`
--

DROP TABLE IF EXISTS `driver_bridge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `driver_bridge` (
  `driver_id` int DEFAULT NULL,
  `sponsor_id` int DEFAULT NULL,
  `points` int DEFAULT NULL,
  `apply` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver_bridge`
--

LOCK TABLES `driver_bridge` WRITE;
/*!40000 ALTER TABLE `driver_bridge` DISABLE KEYS */;
INSERT INTO `driver_bridge` VALUES (17,1,306374,0),(17,2,11811,0),(17,3,695440,0),(25,5,100227,0),(10,3,1000,0),(28,1,0,0),(26,3,0,0),(26,3,0,1);
/*!40000 ALTER TABLE `driver_bridge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `target` varchar(20) DEFAULT NULL,
  `sender` varchar(20) DEFAULT NULL,
  `message` mediumtext,
  `time` datetime DEFAULT NULL,
  `seent` tinyint(1) DEFAULT '0',
  `seens` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES ('will','test','test spon','2020-10-21 19:46:46',1,1),('testdrive','cgaber','yo whats good','2020-10-22 04:37:04',1,1),('evanrh','cgaber','test','2020-10-22 16:19:41',1,1),('cgaber','testdrive','test','2020-10-22 21:38:17',1,1),('cgaber','testdrive','test','2020-10-22 21:38:23',1,1),('cgaber','testdrive','hello','2020-10-23 15:53:47',1,1),('cgaber','testdrive','spam','2020-10-23 15:53:58',1,1),('cgaber','testdrive','spaaam','2020-10-23 15:54:03',1,1),('testdrive','cgaber','%2F%2F%2F%2F%2F%2F%2F%2F','2020-10-23 16:36:59',1,1),('testdrive','cgaber','verylongmessageincomingverylongmessageincomingverylongmessageincomingverylongmessageincomingverylongmessageincoming%0A','2020-10-23 16:38:05',1,1),('evanrh','cgaber','hello','2020-10-26 11:46:05',1,1),('evan_corp','cgaber','testing compose','2020-10-26 22:51:19',1,1),('will','cgaber','longmessageincomingjusttestinglmao','2020-10-26 23:07:11',1,1),('will','cgaber','x','2020-10-26 23:13:46',1,1),('will','cgaber','x','2020-10-26 23:13:49',1,1),('will','cgaber','x','2020-10-26 23:13:52',1,1),('test','cgaber','hello!','2020-10-28 11:32:57',1,1),('will','cgaber','hello!','2020-10-28 11:36:52',1,1),('wsherre','cgaber','test','2020-11-02 21:53:59',1,1),('will','wsherre','malloc test','2020-11-02 22:47:39',1,1),('cgaber','cgaber','test','2020-11-04 12:32:27',1,1),('testdrive','cgaber','hello','2020-11-04 12:33:26',1,1),('cgaber','cgaber','sup','2020-11-04 12:53:04',1,1),('cgaber','cgaber','hello','2020-11-04 12:53:16',1,1),('cgaber','cgaber','okthebn','2020-11-04 12:53:27',1,1),('cgaber','cgaber','sadsad','2020-11-04 12:53:30',1,1),('cgaber','cgaber','sadasdasdas','2020-11-04 12:53:34',1,1),('cgaber','cgaber','ok','2020-11-04 12:55:11',1,1),('testdrive','cgaber','fine','2020-11-04 12:55:35',1,1),('testdrive','cgaber','sup','2020-11-04 12:55:57',1,1),('cgaber','cgaber','testing','2020-11-04 12:59:01',1,1),('cgaber','cgaber','testing again','2020-11-04 12:59:07',1,1),('testdrive','cgaber','hello','2020-11-04 13:02:33',1,1),('cgaber','cgaber','xxx','2020-11-04 13:10:53',1,1),('cgaber','cgaber','hello there','2020-11-04 13:10:59',1,1),('evan_corp','cgaber','testssss','2020-11-04 15:16:35',1,1),('test','cgaber','more testing','2020-11-04 15:17:04',1,1),('evanrh','cgaber','ok','2020-11-04 15:17:40',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:32',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:35',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:35',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:35',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:35',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:36',1,1),('evanrh','cgaber','sup','2020-11-04 15:33:36',1,1),('evanrh','cgaber','oops','2020-11-04 15:34:49',1,1),('evanrh','cgaber','oops','2020-11-04 15:34:57',1,1),('evanrh','cgaber','test again','2020-11-04 15:36:23',1,1),('evanrh','cgaber','test once more','2020-11-04 15:36:29',1,1),('cgaber','cgaber','more testing','2020-11-04 15:59:17',1,1),('cgaber','cgaber','xxxxxxxxx','2020-11-04 15:59:27',1,1),('cgaber','cgaber','zzzzzzzzzzzzzzzzzzzzzzzzzzz','2020-11-04 15:59:33',1,1),('cgaber','cgaber','ok again','2020-11-04 15:59:41',1,1),('cgaber','cgaber','xxx','2020-11-04 16:01:02',1,1),('cgaber','cgaber','try again','2020-11-04 16:01:08',1,1),('cgaber','cgaber','does it work','2020-11-04 16:01:14',1,1),('cgaber','cgaber','does it work','2020-11-04 16:01:26',1,1),('cgaber','cgaber','again','2020-11-04 16:01:33',1,1),('cgaber','cgaber','ok lets try again','2020-11-04 16:01:40',1,1),('cgaber','cgaber','again','2020-11-04 16:02:26',1,1),('cgaber','cgaber','xxxxx','2020-11-04 16:02:31',1,1),('cgaber','cgaber','1','2020-11-04 16:02:37',1,1),('cgaber','cgaber','trying change for will','2020-11-04 16:34:46',1,1),('cgaber','cgaber','test','2020-11-04 16:37:16',1,1),('cgaber','cgaber','test','2020-11-04 16:38:46',1,1),('cgaber','cgaber','ok so far so good','2020-11-04 16:38:54',1,1),('evanrh','cgaber','trying again','2020-11-04 16:39:10',1,1),('evanrh','cgaber','works sometimes i guess','2020-11-04 16:39:18',1,1),('System','testdrive','i have an issue!','2020-11-06 18:04:40',0,1),('cgaber','evan_corp','Ayy I\'m trying this out now','2020-11-07 09:55:46',1,1),('cgaber','evanrh','Whoa','2020-11-08 16:29:23',1,1),('cgaber','will','another test','2020-11-10 20:01:25',1,1),('cgaber','will','yo','2020-11-10 20:04:37',1,1),('test_spon_3','will','hey','2020-11-10 20:21:45',1,1),('app_test','System','Congratulations your sponsor application has been review and accepted by test_spon_3!','2020-11-10 20:41:42',1,1),('app_test','System','ERROR: You have in sufficient points for a purchase. Current points: 0  Purchase Price: -1','2020-11-10 22:41:46',1,1),('app_test','System','ERROR: You have in sufficient points for a purchase. Current points: 0  Purchase Price: 5','2020-11-10 22:47:06',1,1),('app_test','System','ERROR: You have in sufficient points for a purchase for sponsor test_spon_3. Current points: 0  Purchase Price: 5','2020-11-10 22:51:53',1,1),('app_test','System','ERROR: You have in sufficient points for a purchase for sponsor test_3. Current points: 0  Purchase Price: 10','2020-11-10 22:53:54',1,1),('app_test','System','You have gained 10 points for sponsor test_spon_3','2020-11-11 01:06:17',1,1),('app_test','System','You have gained 20 points for sponsor test_spon_3','2020-11-11 11:55:34',1,1),('app_test','will','hey whatsup','2020-11-11 11:55:49',1,1),('app_test','will','hey again','2020-11-11 11:56:59',1,1),('app_test','System','You have gained 5 points for sponsor test_spon_3. Your total is now: 35','2020-11-11 11:59:52',1,1),('System','testdrive','','2020-11-12 01:51:00',0,1),('System','testdrive','','2020-11-12 01:51:22',0,1),('cgaber','testdrive','ok','2020-11-12 01:54:01',1,1),('System','testdrive','','2020-11-12 01:54:14',0,1),('app_test','will','hey dummy','2020-11-12 17:17:24',1,1),('System','cgaber','Lol','2020-11-12 17:21:10',0,1),('app_test','System','Congratulations your sponsor application has been reviewed and accepted by test_spon_3!','2020-11-12 17:23:35',1,1),('System','testdrive','','2020-11-12 18:47:58',0,1),('cgaber','testdrive','testing','2020-11-12 18:48:12',1,1),('test','cgaber','hello!','2020-11-16 11:47:00',1,1),('test_spon_3','will','hey','2020-11-16 11:47:16',1,1),('test_spon_3','will','hey whatsup','2020-11-16 11:48:35',1,1),('app_test','System','You have gained 50 points for sponsor test_spon_3. Your total is now: 102','2020-11-16 11:51:26',1,1),('testdrive','System','You have gained 10000 points for sponsor evan_corp. Your total is now: 12240','2020-11-16 14:35:39',1,1),('testdrive','System','You have gained 30000 points for sponsor evan_corp. Your total is now: 42240','2020-11-16 14:43:30',1,1),('testdrive','System','You have gained 600 points for sponsor evan_corp. Your total is now: 42840','2020-11-16 16:44:17',1,1),('testdrive','System','You have gained 600 points for sponsor evan_corp. Your total is now: 43440','2020-11-16 16:44:21',1,1),('testdrive','System','You have gained 10000 points for sponsor evan_corp. Your total is now: 53440','2020-11-16 16:44:27',1,1),('testdrive','System','You have lost -100 points for sponsor evan_corp. Your total is now 53340','2020-11-17 13:45:20',1,1),('testdrive','System','You have lost -10000 points for sponsor evan_corp. Your total is now 43340','2020-11-17 13:47:06',1,1),('testdrive','System','You have lost -12000 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:51:38',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:52:17',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:52:31',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:53:16',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:54:04',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:54:34',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:55:49',1,1),('testdrive','System','You have lost 0 points for sponsor evan_corp. Your total is now 31340','2020-11-17 13:56:49',1,1),('testdrive','System','You have lost -10000 points for sponsor evan_corp. Your total is now 21340','2020-11-17 13:57:29',1,1),('testdrive','System','You have gained 100000 points for sponsor test. Your total is now: 213562','2020-11-17 15:45:36',1,1),('testdrive','System','You have lost -95000 points for sponsor test. Your total is now 118562','2020-11-17 16:23:13',1,1),('testdrive','System','You have gained 95000 points for sponsor evan_corp. Your total is now: 116340','2020-11-17 16:24:24',1,1),('testdrive','System','ERROR: You have in sufficient points for a purchase for sponsor test. Current points: 118562  Purchase Price: 169900','2020-11-17 16:33:07',1,1),('testdrive','System','You have gained 169900 points for sponsor evan_corp. Your total is now: 286240','2020-11-17 16:34:44',1,1),('testdrive','System','You have lost -100800 points for sponsor test. Your total is now 17762','2020-11-17 16:37:29',1,1),('app_test','System','You have gained 5 points for sponsor test_spon_3. Your total is now: 107','2020-11-17 17:18:19',1,1),('test_spon_3','will','hey','2020-11-17 17:24:22',1,1),('app_test','will','hey','2020-11-17 17:25:35',1,1),('testspon3','System','Welcome to Reward App!','2020-11-18 12:07:38',1,1),('app_test','System','You have gained 5 points for sponsor test_spon_3. Your total is now: 112','2020-11-18 13:15:41',1,1),('testdrive','System','You have gained 100000 points for sponsor test. Your total is now: 117762','2020-11-19 14:53:37',1,1),('testdrive','System','You have gained 15000 points for sponsor test2. Your total is now: 15011','2020-11-19 16:10:32',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 81962','2020-11-19 17:26:30',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 46162','2020-11-19 17:30:33',1,1),('testdrive','System','You have lost -300 points for sponsor evan_corp. Your total is now 285940','2020-11-19 17:44:05',1,1),('app_test','System','Congratulations your sponsor application has been reviewed and accepted by test_spon_3!','2020-11-19 17:46:11',1,1),('app_test','System','You have gained 10 points for sponsor test_spon_3. Your total is now: 122','2020-11-19 17:47:09',1,1),('testdrive','System','You have lost -65000 points for sponsor test. Your total is now 981162','2020-11-19 17:52:07',1,1),('testdrive','System','You have gained 65000 points for sponsor evan_corp. Your total is now: 350940','2020-11-19 17:53:15',1,1),('testdrive','System','You have lost -300 points for sponsor evan_corp. Your total is now 350640','2020-11-19 18:01:34',1,1),('testdrive','System','You have lost -95000 points for sponsor test. Your total is now 886162','2020-11-19 18:14:27',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 850362','2020-11-19 19:35:34',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 814562','2020-11-19 19:40:49',1,1),('testdrive','System','You have lost -65000 points for sponsor test. Your total is now 749562','2020-11-19 19:41:09',1,1),('testdrive','System','You have gained 65000 points for sponsor evan_corp. Your total is now: 415640','2020-11-19 19:41:26',1,1),('testdrive','System','You have gained 35800 points for sponsor evan_corp. Your total is now: 451440','2020-11-19 19:41:36',1,1),('testdrive','System','You have gained 35800 points for sponsor evan_corp. Your total is now: 487240','2020-11-19 19:41:43',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 713762','2020-11-19 20:49:05',1,1),('testdrive','System','You have gained 35800 points for sponsor evan_corp. Your total is now: 523040','2020-11-19 20:49:08',1,1),('app_test','System','Congratulations your sponsor application has been reviewed and accepted by testspon3!','2020-11-20 11:42:23',1,1),('app_test','System','You have lost -122 points for sponsor testspon3. Your total is now 0','2020-11-20 11:42:34',1,1),('erhasti','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-21 18:35:10',1,1),('erhasti','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-21 18:37:11',1,1),('erhasti','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-21 18:38:37',1,1),('erhasti','System','You have been removed as a driver from test!','2020-11-21 18:38:54',1,1),('app_test','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-21 18:39:12',0,1),('app_test','System','You have been removed as a driver from test!','2020-11-21 18:39:35',0,1),('erhasti','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-21 18:44:37',1,1),('erhasti','System','You have been removed as a driver from test!','2020-11-21 18:44:47',1,1),('erhasti','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-21 19:08:38',1,1),('erhasti','System','You have been removed as a driver from test!','2020-11-21 19:08:44',1,1),('System','testdrive','hello','2020-11-23 12:39:48',0,1),('testdrive','System','You have lost -65000 points for sponsor test. Your total is now 648762','2020-11-23 12:43:11',1,1),('testdrive','System','You have gained 65000 points for sponsor evan_corp. Your total is now: 588040','2020-11-23 12:43:14',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 612962','2020-11-23 12:44:59',1,1),('testdrive','System','You have gained 35800 points for sponsor evan_corp. Your total is now: 623840','2020-11-23 12:45:05',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 577162','2020-11-23 12:47:18',1,1),('testdrive','System','You have gained 35800 points for sponsor evan_corp. Your total is now: 659640','2020-11-23 12:48:56',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 541362','2020-11-23 12:49:40',1,1),('testdrive','System','You have gained 35800 points for sponsor evan_corp. Your total is now: 695440','2020-11-23 12:49:47',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 505562','2020-11-23 12:57:54',1,1),('testdrive','System','You have lost -65000 points for sponsor test. Your total is now 440562','2020-11-23 13:01:07',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 404762','2020-11-23 13:04:06',1,1),('testdrive','System','You have lost -3200 points for sponsor test2. Your total is now 11811','2020-11-23 13:27:32',1,1),('testdrive','System','You have gained 100 points for sponsor test. Your total is now: 404862','2020-11-24 11:21:40',1,1),('testdrive','System','You have gained 12312 points for sponsor test. Your total is now: 417174','2020-11-24 11:28:51',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 381374','2020-11-24 15:59:56',1,1),('cgaber','testdrive','wassup homie%0A','2020-11-24 16:00:55',1,1),('signupbroke','System','Welcome to Reward App!','2020-11-24 16:38:38',1,1),('Sam','System','Congratulations your sponsor application has been reviewed and accepted by test!','2020-11-24 18:10:22',1,1),('Sam','System','You have been removed as a driver from test2!','2020-11-24 18:16:18',0,1),('Sam','System','You have been removed as a driver from test2!','2020-11-24 18:17:20',0,1),('signupbroke','System','You have been removed as a driver from NULL!','2020-11-24 18:18:33',0,1),('signupbroke','System','You have been removed as a driver from NULL!','2020-11-24 18:18:55',0,1),('signupbroke','System','You have been removed as a driver from NULL!','2020-11-24 18:19:41',0,1),('signupbroke','System','You have been removed as a driver from NULL!','2020-11-24 18:20:42',0,1),('signup','System','Welcome to Reward App!','2020-11-24 21:37:01',1,1),('erhasti','System','You have lost -300 points for sponsor evan_corp. Your total is now 400','2020-11-25 13:56:11',1,1),('erhasti','System','You have gained 300 points for sponsor evan_corp. Your total is now: 700','2020-11-25 13:56:24',1,1),('erhasti','System','You have lost 0 points for sponsor evan_corp. Your total is now 700','2020-11-25 14:21:27',1,1),('erhasti','System','You have lost 0 points for sponsor evan_corp. Your total is now 700','2020-11-25 14:22:01',1,1),('erhasti','System','You have lost -300 points for sponsor evan_corp. Your total is now 400','2020-11-25 14:27:12',1,1),('erhasti','System','You have gained 600 points for sponsor evan_corp. Your total is now: 1000','2020-11-25 14:27:42',1,1),('erhasti','System','You have lost 0 points for sponsor evan_corp. Your total is now 1000','2020-11-25 14:27:45',1,1),('imacow','System','Welcome to Reward App!','2020-11-25 15:28:12',1,1),('imacow','System','You have been removed as a driver from test!','2020-11-25 16:22:53',1,1),('imacow','System','You have been removed as a driver from test!','2020-11-25 16:26:44',1,1),('testdrive','cgaber','ey','2020-11-25 17:22:40',1,1),('jack','System','You have been removed as a driver from test!','2020-11-25 17:38:24',0,1),('testdrive','System','You have lost -400 points for sponsor test. Your total is now 380974','2020-11-28 20:28:30',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 345174','2020-11-28 20:30:07',1,1),('testdrive','System','You have lost -2600 points for sponsor test. Your total is now 342574','2020-11-28 20:31:03',1,1),('testdrive','System','You have lost -400 points for sponsor test. Your total is now 342174','2020-11-28 20:35:11',1,1),('testdrive','System','You have lost -35800 points for sponsor test. Your total is now 306374','2020-11-28 20:36:39',1,1);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification` (
  `user` varchar(20) DEFAULT NULL,
  `points` tinyint(1) DEFAULT NULL,
  `orders` tinyint(1) DEFAULT NULL,
  `issue` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES ('evanrh',1,1,1),('erhasti',1,1,1),('crobin',1,1,1),('David',1,1,1),('wsherre',1,1,1),('testdrive',1,1,1),('anotherdriver',1,1,1),('anotherdriver2',1,1,1),('tesmsgdriv',1,1,1),('testdriver',1,1,1),('taytay',1,1,1),('remove',1,1,1),('active_test',1,1,1),('app_test',0,1,1),('disable',1,1,1),('disable',1,1,1),('disable',1,1,1),('Sam#@!#!@#@!',1,1,1),('Sam####',1,1,1),('Sam',1,1,1),('signupbroke',1,1,1),('Sam##',1,1,1),('Sam',1,1,1),('signup',1,1,1),('imacow',1,1,1),('jack',1,1,1);
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `points_leaderboard`
--

DROP TABLE IF EXISTS `points_leaderboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `points_leaderboard` (
  `driver_id` int DEFAULT NULL,
  `sponsor_id` int DEFAULT NULL,
  `points` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_leaderboard`
--

LOCK TABLES `points_leaderboard` WRITE;
/*!40000 ALTER TABLE `points_leaderboard` DISABLE KEYS */;
INSERT INTO `points_leaderboard` VALUES (17,1,1325974),(0,2,0),(17,2,15012),(17,3,733537),(25,5,100349),(28,1,0),(26,3,0),(10,3,1900),(26,0,0);
/*!40000 ALTER TABLE `points_leaderboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `name` varchar(30) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `sponsor_id` int DEFAULT NULL,
  `image` blob,
  `date_added` date DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL,
  `Genre` varchar(20) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `product_id` int NOT NULL AUTO_INCREMENT,
  `listing_id` int NOT NULL,
  `img_url` mediumtext,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `sponsor_id` (`sponsor_id`,`listing_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('Nvidia GeForce RTX 3090 24GB D','Condition: New: A brand-new, unused, un...',100000000,3,NULL,NULL,0,NULL,NULL,14,892847633,'https://i.etsystatic.com/25705157/d/il/404279/2661507295/il_170x135.2661507295_83j1.jpg?version=0'),('Jack The Czar Of Halloween Ani','Ready your hooks and make this Jack the ...',100000000,3,NULL,NULL,0,NULL,NULL,16,857253388,'https://i.etsystatic.com/10986298/d/il/ae8acd/2529074802/il_170x135.2529074802_9c00.jpg?version=0'),('Animal Crossing Amiibo Coins','These coins are all compatible with New ...',3,3,NULL,NULL,1,NULL,NULL,17,799218020,'https://i.etsystatic.com/10256292/d/il/5ad5c0/2570983871/il_170x135.2570983871_gmok.jpg?version=0'),('Gigabyte Gaming OC GeForce RTX','Gigabyte Gaming OC GeForce RTX 3090 Fr...',950,1,NULL,NULL,0,NULL,NULL,18,893240109,'https://i.etsystatic.com/25643779/d/il/0e14fe/2615497482/il_170x135.2615497482_nu0g.jpg?version=0'),('Sale Unicorn Face Vinyl Decal ','DECAL ONLY just three easy steps: #1pee...',4,3,NULL,NULL,1,NULL,NULL,19,703507201,'https://i.etsystatic.com/12575555/d/il/530f16/1865732578/il_170x135.1865732578_kjnd.jpg?version=0'),('Sydesk, Ergonomic, Standing De','From sitting to standing. This Computer ...',650,3,NULL,NULL,1,NULL,NULL,20,804109285,'https://i.etsystatic.com/19211082/d/il/7228c5/2294198132/il_170x135.2294198132_150m.jpg?version=0'),('225 Personalized 3/8&Quot; Sat','You will receive 225 personalized 3/8&qu...',82,1,NULL,NULL,1,NULL,NULL,21,247249883,'https://i.etsystatic.com/10784329/d/il/ea02f7/1009474301/il_170x135.1009474301_7pk7.jpg?version=0'),('50 - Shatterproof Frosted Fros','50 Personalized Cups...If you need 50......',60,1,NULL,NULL,1,NULL,NULL,22,467389679,'https://i.etsystatic.com/8426062/d/il/e49349/1012341718/il_170x135.1012341718_hyz3.jpg?version=0'),('Sexy Lingerie... Naughty Nurse','NAUGHTY NURSE & FRENCH MAID One size fi...',27,1,NULL,NULL,1,NULL,NULL,23,847408155,'https://i.etsystatic.com/13192469/d/il/873896/2445383118/il_170x135.2445383118_4tkj.jpg?version=0'),('Be Kind - Unisex T-Shirts - So','This soft and light t-shirt by Bella and...',25,1,NULL,NULL,1,NULL,NULL,24,719950629,'https://i.etsystatic.com/19173898/c/1904/1514/40/293/il/d448d5/2252613727/il_170x135.2252613727_lqbn.jpg'),('Custom Pokémon Card Resin 8x11','One-of-a-kind decorative tray made with ...',120,3,NULL,NULL,1,NULL,NULL,25,862949856,'https://i.etsystatic.com/16204558/d/il/106703/2550568788/il_170x135.2550568788_5aoe.jpg?version=0'),('AMD Ryzen 7 3700x','AMD Ryzen 7 3700x Processor.',358,1,NULL,NULL,1,NULL,NULL,26,888286606,'https://i.etsystatic.com/26002400/d/il/3469c9/2698903163/il_170x135.2698903163_c6wg.jpg?version=1'),('High-End Gaming PC: Ryzen 5800','All parts are in new condition. Componen...',3600,1,NULL,NULL,0,NULL,NULL,27,888127738,'https://i.etsystatic.com/26016234/d/il/13be24/2698297025/il_170x135.2698297025_t90b.jpg?version=0'),('ViprTech Gaming PC Computer De','Introducing the ViprTech Avalanche (AMD)...',725,1,NULL,NULL,1,NULL,NULL,28,718484472,'https://i.etsystatic.com/20765044/d/il/6c48ee/2449291779/il_170x135.2449291779_56s9.jpg?version=0'),('The Tré | Apple Bluetooth Magi','The tré is designed to be a minimal, ele...',75,1,NULL,NULL,1,NULL,NULL,29,783328345,'https://i.etsystatic.com/14200347/d/il/071daa/2608796006/il_170x135.2608796006_5lr4.jpg?version=0'),('ViprTech Gaming PC Computer De','Introducing the ViprTech Blizzard (AMD) ...',650,1,NULL,NULL,1,NULL,NULL,30,779881853,'https://i.etsystatic.com/20765044/c/1500/1192/0/294/il/78abf3/2194868118/il_170x135.2194868118_4fls.jpg'),('Desktop Gaming PC - I5-9400f O','[Images may show other models] Tackle ...',1699,1,NULL,NULL,1,NULL,NULL,31,664326960,'https://i.etsystatic.com/11426206/d/il/a5ded5/2235111598/il_170x135.2235111598_7a49.jpg?version=0'),('AMD RYZEN 9 Cpu PC Logo Label ','Brand new and high quality badge. Great ...',4,1,NULL,NULL,1,NULL,NULL,32,727255821,'https://i.etsystatic.com/11395415/d/il/c40f60/2015671795/il_170x135.2015671795_l0qf.jpg?version=0'),('Intel Core I9-10900K CPU Keych','These are Keychains made by /u/e-racer o...',50,1,NULL,NULL,1,NULL,NULL,33,834876041,'https://i.etsystatic.com/23017301/d/il/20d991/2398314172/il_170x135.2398314172_pajl.jpg?version=1'),('Kiilloitettuja Simpukka Kaulak','Värikkäitä, kiiltäviä ja kevyitä simpukk...',25,1,NULL,NULL,1,NULL,NULL,34,839731597,'https://i.etsystatic.com/23630993/d/il/5703d0/2415312496/il_170x135.2415312496_cgjl.jpg?version=0'),('EuroVision The Elves Went Too ','EuroVision The Elves Went Too Far Vinyl ...',4,2,NULL,NULL,1,NULL,NULL,35,847891684,'https://i.etsystatic.com/20815439/d/il/0ccca2/2493398118/il_170x135.2493398118_gv2r.jpg?version=0'),('Kiilloitettuja Simpukka Kaulak','Värikkäitä, kiiltäviä ja kevyitä simpukk...',25,2,NULL,NULL,1,NULL,NULL,36,839731597,'https://i.etsystatic.com/23630993/d/il/5703d0/2415312496/il_170x135.2415312496_cgjl.jpg?version=0'),('Eurovision Stickers Fire Saga ','Hey baby Double Trouble! Oh yeah! Fire S...',4,2,NULL,NULL,1,NULL,NULL,37,822744246,'https://i.etsystatic.com/21496737/d/il/554290/2404374270/il_170x135.2404374270_c84n.jpg?version=0'),('JOSH ALLEN Buffalo Bills Photo','Our original Sports Player Art series fe...',7,2,NULL,NULL,1,NULL,NULL,38,883832408,'https://i.etsystatic.com/19990501/d/il/eba6f3/2681119925/il_170x135.2681119925_2gnn.jpg?version=0'),('Kuusi Kappaletta Helmiriipuksi','Puuhelmiriipuksia kestävällä puuvillanyö...',25,2,NULL,NULL,1,NULL,NULL,39,825814596,'https://i.etsystatic.com/23630993/d/il/0358c4/2415193398/il_170x135.2415193398_df55.jpg?version=0'),('Next Day Shipping Sports Baseb','Play &quot;Eye Spy&quot; We have hidden ...',3,2,NULL,NULL,1,NULL,NULL,40,635672521,'https://i.etsystatic.com/16754554/d/il/13cd39/1634187531/il_170x135.1634187531_n3xc.jpg?version=0'),('Funny Eurovision Christmas Car','When will it be enough for you?! It wil...',3,2,NULL,NULL,1,NULL,NULL,41,872220614,'https://i.etsystatic.com/20798960/c/1498/1190/128/326/il/88c231/2670791763/il_170x135.2670791763_h473.jpg'),('Zinc Fence ORIGINAL OIL Jamaic','This is a painting I did using oil paint...',5015,2,NULL,NULL,1,NULL,NULL,42,386921172,'https://i.etsystatic.com/6183799/d/il/d7251d/1040430945/il_170x135.1040430945_91r9.jpg?version=0'),('Take One For The Team Greeting','Now that&#39;s love. 5&quot; x 7&quot; ...',4,2,NULL,NULL,1,NULL,NULL,43,682296983,'https://i.etsystatic.com/5176394/c/1119/888/117/446/il/c69027/1776806446/il_170x135.1776806446_jbv2.jpg'),('Any 3 Bookmarks For 10 Quid!','Any three bookmarks of your choice for £...',10,2,NULL,NULL,1,NULL,NULL,44,793627760,'https://i.etsystatic.com/14490731/c/1818/1445/108/0/il/3a6e51/2708069849/il_170x135.2708069849_3967.jpg'),('Pig Stencil, Custom Stencil, A','New Pig design stencil. It is made of d...',3,2,NULL,NULL,1,NULL,NULL,45,813186265,'https://i.etsystatic.com/21249055/d/il/425a10/2371619755/il_170x135.2371619755_3cz2.jpg?version=0'),('Slim Custom Dog Can Cooler For','Put your dog&#39;s face on a custom can ...',6,2,NULL,NULL,1,NULL,NULL,46,798916228,'https://i.etsystatic.com/20008836/d/il/d65c0b/2648016161/il_170x135.2648016161_mell.jpg?version=0'),('Personalised Age Happy Birthda','A fun and impressive handmade bunting fo...',9,2,NULL,NULL,1,NULL,NULL,47,800266276,'https://i.etsystatic.com/12602942/d/il/27023b/2327269872/il_170x135.2327269872_phrj.jpg?version=0'),('Silver Mirror Personalised Chr','Beautiful SILVER Mirror Finish Personali...',13,2,NULL,NULL,1,NULL,NULL,48,881836112,'https://i.etsystatic.com/15059424/d/il/a5aad5/2625466288/il_170x135.2625466288_cja5.jpg?version=0'),('Custom Family Name Sign, Estab','Custom family name size, with est date ...',39,2,NULL,NULL,1,NULL,NULL,49,681957614,'https://i.etsystatic.com/12863024/d/il/72a474/1871600130/il_170x135.1871600130_8y42.jpg?version=0'),('PEAK Personalized Photo Design','This is the Perfect Mother&#39;s Day Gif...',40,2,NULL,NULL,1,NULL,NULL,50,676586580,'https://i.etsystatic.com/16358200/d/il/4ab139/1810962146/il_170x135.1810962146_dt79.jpg?version=0'),('SALE!! SET OF 5 Gold Mason Jar','* please put the date you need these by ...',26,1,NULL,NULL,1,NULL,NULL,51,457600622,'https://i.etsystatic.com/12263538/d/il/90302c/1022512326/il_170x135.1022512326_s4ki.jpg?version=0'),('Ja Morant Vancouver Mask','Handmade mask. Inside cotton fabric outs...',16,1,NULL,NULL,1,NULL,NULL,52,857453491,'https://i.etsystatic.com/24136487/d/il/394b31/2477454700/il_170x135.2477454700_dhpt.jpg?version=0');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsor`
--

DROP TABLE IF EXISTS `sponsor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sponsor` (
  `title` varchar(20) DEFAULT NULL,
  `sponsor_id` int NOT NULL,
  `address` varchar(40) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `image` blob,
  `date_join` date DEFAULT NULL,
  `date_leave` date DEFAULT NULL,
  `point_value` double DEFAULT '0.01',
  PRIMARY KEY (`sponsor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsor`
--

LOCK TABLES `sponsor` WRITE;
/*!40000 ALTER TABLE `sponsor` DISABLE KEYS */;
INSERT INTO `sponsor` VALUES ('test',1,'NULL','NULL','NULL',_binary 'NULL','2020-10-19','0000-00-00',0.01),('test2',2,'NULL','NULL','NULL',_binary 'NULL','2020-10-20','0000-00-00',0.01),('Evan Corp',3,'123 Corporation St','8645689541','admin@evancorp.net',_binary 'NULL','2020-10-21','0000-00-00',0.01),('Team 15 Sponsor',4,'NULL','NULL','NULL',_binary 'NULL','2020-10-27','0000-00-00',0.2),('test_3',5,'NULL','NULL','NULL',_binary 'NULL','2020-11-11','0000-00-00',0.01);
/*!40000 ALTER TABLE `sponsor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsor_logins`
--

DROP TABLE IF EXISTS `sponsor_logins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sponsor_logins` (
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `sponsor_id` int DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  `date_join` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsor_logins`
--

LOCK TABLES `sponsor_logins` WRITE;
/*!40000 ALTER TABLE `sponsor_logins` DISABLE KEYS */;
INSERT INTO `sponsor_logins` VALUES ('test','sha256$ybgeaRuw$5dca4125349b65b934e059d57d9832f33f9cbe34f723175183b728491ec864c2',1,1,'2020-10-19'),('test2','sha256$6ZsIz5rR$a61a7fcd991ee020224b5c7e152d78871b3fdf056bd844adc80ed84978cb63e7',2,1,'2020-10-20'),('evan_corp','sha256$IkbEQtfy$c33dfb50f28aea0f9993b19de354ea9fa9f1daae592dd6d1d3af75e72d14bdd2',3,1,'2020-10-21'),('team15','sha256$fQ7nDHnT$4fa05aa637316da58961da1672373fb807f98eb0c03e8d11589b93a7132ee200',4,1,'2020-10-27'),('test_spon_3','sha256$b11elI5S$71ee1822f4d590ef25c2831f0b371b24cc2f3aac7d6a251f6e67cb528bf28c9e',5,1,'2020-11-11'),('spon3','sha256$cKntsn9h$fb2a2be5a0a0c5b966cf992cd0835cb3d6419f9032e65c22060dca56faffe1ef',5,1,'2020-11-20');
/*!40000 ALTER TABLE `sponsor_logins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suspend`
--

DROP TABLE IF EXISTS `suspend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suspend` (
  `user` varchar(20) DEFAULT NULL,
  `date_return` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suspend`
--

LOCK TABLES `suspend` WRITE;
/*!40000 ALTER TABLE `suspend` DISABLE KEYS */;
/*!40000 ALTER TABLE `suspend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `UserName` varchar(20) NOT NULL,
  `Admin_ID` int DEFAULT NULL,
  `Driver_ID` int DEFAULT NULL,
  `Sponsor_ID` int DEFAULT NULL,
  `last_in` datetime DEFAULT NULL,
  KEY `Admin_ID` (`Admin_ID`),
  KEY `Driver_ID` (`Driver_ID`),
  KEY `Sponsor_ID` (`Sponsor_ID`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`Admin_ID`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`Driver_ID`) REFERENCES `driver` (`driver_id`),
  CONSTRAINT `users_ibfk_3` FOREIGN KEY (`Sponsor_ID`) REFERENCES `sponsor` (`sponsor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('evanrh',NULL,1,NULL,'2020-10-08 21:52:23'),('erhasti',NULL,10,NULL,'2020-10-12 21:53:35'),('crobin',NULL,11,NULL,'2020-10-14 15:17:15'),('David',NULL,14,NULL,'2020-10-14 20:19:08'),('will',2,NULL,NULL,'2020-10-15 22:40:03'),('wsherre',NULL,15,NULL,'2020-10-19 17:53:33'),('test',NULL,NULL,1,'2020-10-19 18:29:38'),('cgaber',3,NULL,NULL,'2020-10-19 21:24:33'),('test2',NULL,NULL,2,'2020-10-20 17:20:38'),('testdrive',NULL,17,NULL,'2020-10-21 03:42:06'),('evan_corp',NULL,NULL,3,'2020-10-21 19:00:11'),('team15',NULL,NULL,4,'2020-10-27 03:52:12'),('testad',4,NULL,NULL,'2020-11-02 18:37:30'),('System',5,NULL,NULL,'2020-11-06 22:30:42'),('evan',6,NULL,NULL,'2020-11-07 20:48:23'),('test_spon_3',NULL,NULL,5,'2020-11-11 01:21:31'),('app_test',NULL,25,NULL,'2020-11-11 01:23:01'),('testspon3',NULL,NULL,5,'2020-11-18 16:15:24'),('spon3',NULL,NULL,5,'2020-11-20 17:12:45'),('imacow',NULL,26,NULL,'2020-11-25 20:02:16'),('jack',NULL,27,NULL,'2020-11-25 22:37:46');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-30  1:36:21
