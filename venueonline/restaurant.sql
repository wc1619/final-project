CREATE TABLE `Restaurant` (
  `RestaurantID` int PRIMARY KEY,
  `Reference` int,
  `Name` varchar(255),
  `Address` varchar(255),
  `MenuID` int
);

CREATE TABLE `Menu` (
  `MenuID` int PRIMARY KEY,
  `FoodID` int,
  `StartTime` datetime,
  `EndTime` datetime
);

CREATE TABLE `Order` (
  `OrderID` int PRIMARY KEY,
  `CreatedTime` datetime DEFAULT (now()),
  `TableReference` int,
  `CustomerID` int UNIQUE NOT NULL
);

CREATE TABLE `OrderDetails` (
  `OrderID` int PRIMARY KEY,
  `FoodID` int,
  `FoodQty` int DEFAULT 1,
  `UnitPrice` float
);

CREATE TABLE `FoodItems` (
  `FoodID` int PRIMARY KEY,
  `FoodName` varchar(255),
  `UnitPrice` float,
  `Description` varchar(255),
  `Specification` varchar(255),
  `ItemCategory` varchar(255)
);

CREATE TABLE `Payment` (
  `PaymentID` int PRIMARY KEY,
  `PaymentMethod` varchar(255),
  `OrderID` int
);

CREATE TABLE `Diningtable` (
  `DiningTableID` int PRIMARY KEY,
  `RestaurantID` int,
  `ChairsCount` int,
  `Reference` int,
  `MenuID` int,
  `TableStatus` ENUM ('Occupied', 'Idle')
);

CREATE TABLE `Customer` (
  `CustomerID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Email` varchar(255)
);

CREATE TABLE `Administrator` (
  `AdminId` int PRIMARY KEY,
  `Name` varchar(255),
  `RestaurantID` int,
  `Password` varchar(255)
);

ALTER TABLE `OrderDetails` ADD FOREIGN KEY (`OrderID`) REFERENCES `Order` (`OrderID`);

ALTER TABLE `OrderDetails` ADD FOREIGN KEY (`FoodID`) REFERENCES `FoodItems` (`FoodID`);

ALTER TABLE `Restaurant` ADD FOREIGN KEY (`MenuID`) REFERENCES `Menu` (`MenuID`);

ALTER TABLE `Menu` ADD FOREIGN KEY (`FoodID`) REFERENCES `FoodItems` (`FoodID`);

ALTER TABLE `Payment` ADD FOREIGN KEY (`OrderID`) REFERENCES `Order` (`OrderID`);

ALTER TABLE `Diningtable` ADD FOREIGN KEY (`RestaurantID`) REFERENCES `Restaurant` (`RestaurantID`);

ALTER TABLE `Diningtable` ADD FOREIGN KEY (`DiningTableID`) REFERENCES `Order` (`TableReference`);

ALTER TABLE `Order` ADD FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`);

ALTER TABLE `Restaurant` ADD FOREIGN KEY (`RestaurantID`) REFERENCES `Administrator` (`RestaurantID`);

ALTER TABLE `Menu` ADD FOREIGN KEY (`MenuID`) REFERENCES `Diningtable` (`MenuID`);
