DROP DATABASE IF EXISTS `priceaid`;
CREATE DATABASE IF NOT EXISTS `priceaid`;

Use `priceaid`;

DROP TABLE IF EXISTS `priceaid`.`administrator`;
CREATE TABLE IF NOT EXISTS `priceaid`.`administrator`(
    `userID` INT NOT NULL AUTO_INCREMENT,
    `loginStatus` BINARY NOT NULL,
	`email` NVARCHAR(255) NOT NULL,
    `password` NVARCHAR(255) NOT NULL,
	`name` NVARCHAR(255) NOT NULL,
	`phonenumber` NVARCHAR(255) NOT NULL,
    PRIMARY KEY(`userID`)
);

DROP TABLE IF EXISTS `priceaid`.`saved_table`;
CREATE TABLE IF NOT EXISTS `priceaid`.`saved_table` (
    `userID` INT NOT NULL,
    `itemID` INT NOT NULL AUTO_INCREMENT,
    `name` NVARCHAR(255) NOT NULL,
    `url` NVARCHAR(255) NOT NULL,
	`price` DECIMAL(6,2) NOT NULL,
	`company_name` NVARCHAR(255) NOT NULL,
	`image_url` NVARCHAR(255) NOT NULL,
    PRIMARY KEY(`itemID`),
    CONSTRAINT `FK_tbladministrator_tblsaved_table_userID` FOREIGN KEY (`userID`) REFERENCES `priceaid`.`administrator` (`userID`)
);

DROP TABLE IF EXISTS `priceaid`.`history`;
CREATE TABLE IF NOT EXISTS `priceaid`.`history`(
    `userID` INT NOT NULL,
    `itemCode` INT NOT NULL AUTO_INCREMENT,
    `searchedDate` NVARCHAR(255) NOT NULL,
    `itemName` NVARCHAR(255) NOT NULL,
    PRIMARY KEY(`itemCode`),
    CONSTRAINT `FK_tbladministrator_tblhistory_userID` FOREIGN KEY (`userID`) REFERENCES `priceaid`.`administrator` (`userID`)
);