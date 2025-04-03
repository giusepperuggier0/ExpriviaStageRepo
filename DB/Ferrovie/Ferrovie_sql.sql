CREATE DATABASE ferrovie;

USE ferrovie;
 
-- Tabella Stazione_ferroviaria

CREATE TABLE Stazione_ferroviaria (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   nome VARCHAR(100) NOT NULL,

   citta VARCHAR(100) NOT NULL,

   binari INT NOT NULL

);
 
-- Tabella Macchinista

CREATE TABLE Macchinista (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   nome VARCHAR(50) NOT NULL,

   cognome VARCHAR(50) NOT NULL

);
 
-- Tabella Treno

CREATE TABLE Treno (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   tipo_treno VARCHAR(50) NOT NULL,

   capacita INT NOT NULL,

   ID_macchinista INT,

   FOREIGN KEY (ID_macchinista) REFERENCES Macchinista(ID)

);
 
-- Tabella Controllore

CREATE TABLE Controllore (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   nome VARCHAR(50) NOT NULL,

   cognome VARCHAR(50) NOT NULL

);
 
-- Tabella Tratta

CREATE TABLE Tratta (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   stazione_partenza INT NOT NULL,

   stazione_arrivo INT NOT NULL,

   durata TIME NOT NULL,

   ID_controllore INT,

   FOREIGN KEY (stazione_partenza) REFERENCES Stazione_ferroviaria(ID),

   FOREIGN KEY (stazione_arrivo) REFERENCES Stazione_ferroviaria(ID),

   FOREIGN KEY (ID_controllore) REFERENCES Controllore(ID)

);
 
-- Tabella Viaggiatore

CREATE TABLE Viaggiatore (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   nome VARCHAR(50) NOT NULL,

   cognome VARCHAR(50) NOT NULL

);
 
-- Tabella Percorre

CREATE TABLE Percorre (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   ID_treno INT NOT NULL,

   ID_tratta INT NOT NULL,

   orario_partenza TIME NOT NULL,

   orario_arrivo TIME NOT NULL,

   ritardo INT,

   FOREIGN KEY (ID_treno) REFERENCES Treno(ID),

   FOREIGN KEY (ID_tratta) REFERENCES Tratta(ID)

);
 
-- Tabella Biglietto

CREATE TABLE Biglietto (

   ID INT PRIMARY KEY AUTO_INCREMENT,

   data DATE NOT NULL,

   prezzo DECIMAL(10,2) NOT NULL,

   ID_viaggiatore INT NOT NULL,

   ID_tratta INT NOT NULL,

   FOREIGN KEY (ID_viaggiatore) REFERENCES Viaggiatore(ID),

   FOREIGN KEY (ID_tratta) REFERENCES Tratta(ID)

);
 