create database mukhmasi;
use mukhmasi;

CREATE TABLE Admins (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(100)
);


CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(50),
	ProductDate DATE ,
    Price DECIMAL(10, 2),
    sell_Price DECIMAL(10, 2),
    StockQuantity INT
);

CREATE TABLE Suppliers (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(255) NOT NULL,
    ContactPerson VARCHAR(100),
    ContactNumber VARCHAR(20)
);

CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
    Phone VARCHAR(20)
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    Status VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


CREATE TABLE OrderDetails (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    Subtotal DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);



CREATE TABLE Transaction (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionDate DATE,
    Type VARCHAR(20),
    Amount DECIMAL(10, 2),
    ProductID INT,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

ALTER TABLE Orders
ADD COLUMN receive BOOLEAN;

-------------------------------

ALTER TABLE Orders
ADD COLUMN remainAmount DECIMAL(10, 2);

create table payments(
paymentId INT AUTO_INCREMENT PRIMARY KEY,
paymentDate DATE,
OrderID int,
Amount DECIMAL(10, 2),
FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
)

----------------
ALTER TABLE Suppliers
DROP COLUMN ContactPerson;

create table purchases(
Id INT AUTO_INCREMENT PRIMARY KEY,
Date DATE,
SupplierID int,
Amount DECIMAL(10, 2),
FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
)

CREATE TABLE Checks (
    check_id INT AUTO_INCREMENT PRIMARY KEY,
    check_number VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    check_date DATE NOT NULL
)

create table Purchase_pay(
Id INT AUTO_INCREMENT PRIMARY KEY,
PurchasesId int,
payment_method ENUM('cash', 'check') NOT NULL,
amount DECIMAL(10, 2),
remain DECIMAL(10, 2),
check_id INT,
   
FOREIGN KEY (check_id) REFERENCES Checks(check_id),
FOREIGN KEY (PurchasesId) REFERENCES purchases(Id)
)

ALTER TABLE Purchase_pay
DROP COLUMN remain;

ALTER TABLE purchases
Add COLUMN remain DECIMAL(10, 2);

ALTER TABLE orderdetails
DROP FOREIGN KEY orderdetails_ibfk_2,
ADD FOREIGN KEY (ProductID) REFERENCES products(ProductID) ON DELETE CASCADE;


--------------------------
create table Obligations(
ObID int auto_increment primary key ,
name varchar(50),
amount double
	);

--------------
ALTER TABLE Products
Add COLUMN Unit VARCHAR(20);

------------
ALTER TABLE orders 
CHANGE COLUMN  remainAmount remainAmount DECIMAL(10,2)  DEFAULT 0 ;
-------------

create table employee(
EID int auto_increment primary key ,
name varchar(100) ,
salary double,
phone varchar(50) ,
lastSalary date ,
des varchar(250)
);

create table  emp_bills (
BID int auto_increment primary key,
date date,
amount double,
EID int,
FOREIGN KEY (EID) REFERENCES employee(EID) ON DELETE SET NULL
);

create table  elc_bills (
BID int auto_increment primary key,
date date,
amount double
);
create table  wat_bills (
BID int auto_increment primary key,
date date,
amount double
);

create table  tr_bills (
BID int auto_increment primary key,
des varchar(250) default "-",
date date,
amount double
);

create table  ot_bills (
BID int auto_increment primary key,
title varchar(250) default "-",
date date,
amount double
);

ALTER TABLE employee
CHANGE COLUMN phone phone  VARCHAR(50)  DEFAULT '-' ,
CHANGE COLUMN des des VARCHAR(250)  DEFAULT '-' ;


Drop table obligations;
-------
ALTER TABLE orders 
ADD COLUMN discount varchar(50) DEFAULT '%0.00';

ALTER TABLE orders 
ADD COLUMN AfterDiscount DECIMAL(10,2);

ALTER TABLE orders
MODIFY COLUMN remainAmount DECIMAL(10,2) DEFAULT '0.00';

-----------
