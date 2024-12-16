# Variables used for database configuration


### Credentials

USERNAME = "root"
# DB_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD") # this wont work since server isnt in the docker container with the mysql database
PASSWORD = "root" # hardcoded instead


### Technical settings
DATABASE_NAME = "fullstack_db"
SYSTEM = "MySQL"



### Schemas defining the tables in database

TABLES = {}
"""Dict of CREATE TABLE statements"""
        
# entity-value model for products with differing types (and properties)
TABLES['Products'] = (
    "CREATE TABLE `Products` ("
    "   `ID` int NOT NULL AUTO_INCREMENT,"
    "   `Type` varchar(256)," # arbritrary size limit yay
    "   `Name` varchar(40),"
    "   `Price` float,"
    "   `Currency` varchar(3),"
    "   `Stock` int,"
    "   PRIMARY KEY (`ID`)"
    ")")

TABLES['Properties'] = (
    "CREATE TABLE `Properties` ("
    "   `ProductID` int NOT NULL,"
    "   `Name` varchar(256) NOT NULL,"
    "   `Value` varchar(256),"
    "   CONSTRAINT PK_Properties PRIMARY KEY (`ProductID`, `Name`),"
    "   FOREIGN KEY (ProductID) REFERENCES Products(ID)"
    ")")

TABLES['ProductImages'] = (
    "CREATE TABLE `ProductImages` ("
    "   `ProductID` int NOT NULL,"
    "   `Path` varchar(256) NOT NULL,"
    "   CONSTRAINT PK_ProductImages PRIMARY KEY (`ProductID`, `Path`),"
    "   FOREIGN KEY (ProductID) REFERENCES Products(ID)"
    ")")

TABLES['Customers'] = ( # represents a customer
    "CREATE TABLE `Customers` ("
    "   `ID` int NOT NULL AUTO_INCREMENT,"
    "   `FirstName` varchar(40),"
    "   `LastName` varchar(40),"
    "   PRIMARY KEY (`ID`)"
    ")")

TABLES['Orders'] = ( # represents an order a customer has placed
    "CREATE TABLE `Orders` ("
    "   `ID` int NOT NULL AUTO_INCREMENT,"
    "   `CustomerID` int NOT NULL,"
    "   PRIMARY KEY (`ID`),"
    "   FOREIGN KEY (CustomerID) REFERENCES Customers(ID)"
    ")")

TABLES['OrderDetails'] = ( # represents the amount of each product in an order
    "CREATE TABLE `OrderDetails` ("
    "   `OrderID` int NOT NULL,"
    "   `ProductID` int NOT NULL,"
    "   `Quantity` int NOT NULL,"
    "   CONSTRAINT PK_OrderDetails PRIMARY KEY (`OrderID`, `ProductID`),"
    "   FOREIGN KEY (OrderID) REFERENCES Orders(ID),"
    "   FOREIGN KEY (ProductID) REFERENCES Products(ID)"
    ")")