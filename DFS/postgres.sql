-- total participation and key constraints between orders and delivers is enforced in the front end

drop table IF EXISTS Users CASCADE;
drop table IF EXISTS FDS_Manager CASCADE;
drop table IF EXISTS FDS_Promo CASCADE;
drop table IF EXISTS Restaurant CASCADE;
drop table IF EXISTS Promotion CASCADE;
drop table IF EXISTS Food CASCADE;
drop table IF EXISTS Customer CASCADE;
drop table IF EXISTS Contain CASCADE;
drop table IF EXISTS Orders CASCADE;
drop table IF EXISTS Reviews CASCADE;
drop table IF EXISTS Delivery_Staff CASCADE;
drop table IF EXISTS Delivers CASCADE;
drop table IF EXISTS Part_Time CASCADE;
drop table IF EXISTS Full_Time CASCADE;
drop table IF EXISTS WWS CASCADE;
drop table IF EXISTS MWS CASCADE;
drop table IF EXISTS CreditCard CASCADE;

CREATE TABLE Users (
	uname varchar(100) PRIMARY KEY,
	password varchar(100)
);

--customer
insert into Users (uname, password) values ('customer1', 'password');
insert into Users (uname, password) values ('customer2', 'G0C0nM2aSXQq');
insert into Users (uname, password) values ('customer3', '3xT31av0');
insert into Users (uname, password) values ('customer4', 'qzRMZjS');
insert into Users (uname, password) values ('customer5', 'UQ3zO3gMZlco');
insert into Users (uname, password) values ('customer6', 'pEBDIB');
insert into Users (uname, password) values ('customer7', '0hW1ypIl7m');
insert into Users (uname, password) values ('customer8', 'oz8zZgx3y6r');
insert into Users (uname, password) values ('customer9', 'xHMF14d');
insert into Users (uname, password) values ('customer10', 'jJuSP7s14nMV');

--restaurant
insert into Users (uname, password) values ('restaurant1', 'password');
insert into Users (uname, password) values ('restaurant2', 'kO7kzS');
insert into Users (uname, password) values ('restaurant3', 'OicFrEC');
insert into Users (uname, password) values ('restaurant4', 'B8xVeAwbZ4');
insert into Users (uname, password) values ('restaurant5', 'VBkuWlJev');
insert into Users (uname, password) values ('restaurant6', 'nV85mxp8NCkF');
insert into Users (uname, password) values ('restaurant7', '7DKUCxb7MF');
insert into Users (uname, password) values ('restaurant8', 'yfLkbORCo');
insert into Users (uname, password) values ('restaurant9', 'E9N93I');
insert into Users (uname, password) values ('restaurant10', 'V8wSkxx');

--Part Time Delivery Staff
insert into Users (uname, password) values ('parttime1', 'password');
insert into Users (uname, password) values ('parttime2', 'PKTJYt4I');
insert into Users (uname, password) values ('parttime3', 'vaQ1BIyW1BJ');
insert into Users (uname, password) values ('parttime4', 'Fi2EeoLugdD');
insert into Users (uname, password) values ('parttime5', 'EqZkrcDEaZLu');
insert into Users (uname, password) values ('parttime6', 'AnPRcIAp1');
insert into Users (uname, password) values ('parttime7', 'TnFwo3pNv6R');
insert into Users (uname, password) values ('parttime8', 'cLzMWyXQLrnN');
insert into Users (uname, password) values ('parttime9', '1hvaQKvGZ');
insert into Users (uname, password) values ('parttime10', 'LpORvihrd');

--Full Time Delivery Staff
insert into Users (uname, password) values ('fulltime1', 'password');
insert into Users (uname, password) values ('fulltime2', '2jEfoNnmh');
insert into Users (uname, password) values ('fulltime3', 'eOQZBnMyO');
insert into Users (uname, password) values ('fulltime4', '0FXp5Bu');
insert into Users (uname, password) values ('fulltime5', 'XAjQPoqk8O');
insert into Users (uname, password) values ('fulltime6', 'PdcUbvwPNJ');
insert into Users (uname, password) values ('fulltime7', 'o4Wja9jPb');
insert into Users (uname, password) values ('fulltime8', 'DMf2VY');
insert into Users (uname, password) values ('fulltime9', 'ww8eLEM');
insert into Users (uname, password) values ('fulltime10', 'HFODCX');
insert into Users (uname, password) values ('fulltime11', 'KeAG16veJ');
insert into Users (uname, password) values ('fulltime12', '2jEfoNnmh');
insert into Users (uname, password) values ('fulltime13', 'eOQZBnMyO');
insert into Users (uname, password) values ('fulltime14', '0FXp5Bu');
insert into Users (uname, password) values ('fulltime15', 'XAjQPoqk8O');
insert into Users (uname, password) values ('fulltime16', 'PdcUbvwPNJ');
insert into Users (uname, password) values ('fulltime17', 'o4Wja9jPb');
insert into Users (uname, password) values ('fulltime18', 'DMf2VY');
insert into Users (uname, password) values ('fulltime19', 'ww8eLEM');
insert into Users (uname, password) values ('fulltime20', 'HFODCX');

--Manager
insert into Users (uname, password) values ('manager', 'password');



CREATE TABLE Restaurant (
	uname varchar(100) PRIMARY KEY References Users ON DELETE CASCADE,
	rname varchar(100) NOT NULL UNIQUE,
	address varchar(100) NOT NULL,
	min_amt numeric NOT NULL
);

INSERT INTO Restaurant values
	('restaurant1', 'Kenki Sushi','Blk 1 Kent Ridge St 1',10), -- Japanese
	('restaurant2', 'Tin Tai Feng','23 Lorong One Road 3',5), --Chinese
	('restaurant3', 'Prada Wala','Blk 6 Kent Ridge St 9',5), --Indian
	('restaurant4', 'Hastons','Blk 88 Pasir Ris Road 3',5), --Western
	('restaurant5', 'Gacks Place','Blk 8 Red Hill St 56',10), -- Western
	('restaurant6', 'Pacdonalds','Blk 2 Pasir Panjang St 5',5), -- Western
	('restaurant7', 'Burger Queen','Blk 140 Habourfront St 6',5), -- Western
	('restaurant8', 'Stuffed','Blk 18 Bishan Circle St 78',6), -- Western
	('restaurant9', 'Amaans','Blk 5 Yishun View St 79',6), -- Malay 
	('restaurant10', 'Nineteen Chefs','Blk 123 Hougang Road St 67',5); --Western


CREATE TABLE Promotion (
	promoId numeric PRIMARY KEY,
	start_date date NOT NULL,
	end_date date NOT NULL,
	name varchar,
	promoCode varchar,
	runame varchar(100),
	FOREIGN KEY(runame) REFERENCES Restaurant(uname) ON DELETE CASCADE
);

INSERT INTO Promotion values
	(1, '2020-01-01', '2020-04-27', 'free delivery', 'FREEDELIVERY','restaurant1'),
	(2, '2020-01-05', '2020-01-19', '10% off', '10OFF','restaurant1'),
	(3, '2020-04-10', '2020-04-22', '10% off', '10OFF','restaurant2'),
	(4, '2020-03-01', '2020-05-02', 'free delivery', 'FREEDELIVERY','restaurant2'),
	(5, '2020-01-01', '2020-02-03', '15% off', '15OFF','restaurant2'),
	(6, '2020-01-03', '2020-04-04', '20% off', '20OFF','restaurant3'),
	(7, '2020-02-02', '2020-04-16', '15% off', '15OFF','restaurant3'),
	(8, '2020-01-01', '2020-01-04', '10% off', '10OFF','restaurant3');

CREATE TABLE Food (
	runame varchar(100),
	fname varchar(100),
	availability boolean DEFAULT true,
	price numeric NOT NULL,
	order_limit numeric,
	category varchar(100),
	PRIMARY KEY (runame, fname),
	FOREIGN KEY (runame) REFERENCES Restaurant(uname) ON DELETE CASCADE
);

INSERT INTO Food values 
('restaurant1','Sushi',true,11,100,'Japanese'),
('restaurant1','Ramen',true,16,50,'Japanese'), 
('restaurant1','Mochi',true,5,100,'Dessert'),
('restaurant1','California Roll',true,4,100,'Japanese'), 
('restaurant1','Okonomiyaki',true,13,100,'Japanese'), 

('restaurant2','Hokkien Mee',true,5,100,'Chinese'), 
('restaurant2','Prawn Noodles',true,4.50,100,'Chinese'), 
('restaurant2','Egg Fried Rice',true,5.50,100,'Chinese'),
('restaurant2','Seafood Hor Fun',true,6,100,'Chinese'),
('restaurant2','Bobo Cha Cha',true,3.50,100,'Dessert'),

('restaurant3','Plain Prata',true,2,100,'Indian'),
('restaurant3','Egg Prata',true,2,100,'Indian'), 
('restaurant3','Ice Cream Prata',true,4,100,'Dessert'),
('restaurant3','Nasi Briyani',true,6,100,'Indian'), 
('restaurant3','Nasi Goreng',true,5,100,'Indian'), 

('restaurant4','Seafood Aglio Olio',true,18,100,'Western'), 
('restaurant4','Chicken Chop',true,20,100,'Western'), 
('restaurant4','Fish and Chips',true,18,100,'Western'),
('restaurant4','Cheese Fries',true,10,100,'Western'),
('restaurant4','Banana Split',true,12,200,'Dessert'),

('restaurant5','Ribeye Steak',true,30,100,'Western'), 
('restaurant5','Chicken Alfredo',true,18,100,'Western'),
('restaurant5','Mushroom Aglio Olio',true,15,100,'Western'), 
('restaurant5','Seafood Salad',true,15,100,'Western'), 
('restaurant5','Onion Rings',true,10,100,'Western'), 

('restaurant6','Filet O’ Fish',true,5,100,'Western'), 
('restaurant6','Pc Spicy',true,6,100,'Western'), 
('restaurant6','6 pc Nuggets',true,6,100,'Western'),
('restaurant6','9 pc Nuggets',true,9,100,'Western'),
('restaurant6','Oreo Pc Flurry',true,2.50,200,'Dessert'),

('restaurant7','Fish Burger',true,8,100,'Western'), 
('restaurant7','Beef Burger',true,10,100,'Western'), 
('restaurant7','Veggie Burger',true,8,100,'Western'),
('restaurant7','Chicken Burger',true,10,100,'Western'),
('restaurant7','Chocolate Pie',true,6,200,'Dessert'),

('restaurant8','Burrito',true,6,100,'Western'), 
('restaurant8','Chicken Kebab',true,5,100,'Western'), 
('restaurant8','Salad Bowl',true,6,100,'Western'),
('restaurant8','Beef Kebab',true,5,100,'Western'),
('restaurant8','Quesadilla',true,6,200,'Western'),

('restaurant9','Kampong Fried Rice',true,6,100,'Malay'), 
('restaurant9','Maggie Pataya',true,5,100,'Malay'), 
('restaurant9','Butter Chicken',true,4,100,'Malay'),
('restaurant9','Cheese Fries',true,5,100,'Malay'),
('restaurant9','Nasi Goreng',true,7,200,'Malay'),

('restaurant10','Mushroom Aglio Olio',true,6,100,'Western'), 
('restaurant10','Grilled Chicken',true,5,100,'Western'), 
('restaurant10','Steak',true,6,100,'Western'),
('restaurant10','Cheese Baked Rice',true,5,100,'Western'),
('restaurant10','Cheese Baked Pasta',true,6,200,'Western');

CREATE TABLE Customer (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	cname varchar(100) NOT NULL,
	points numeric,
	date_created date
);

INSERT INTO Customer values 
	('customer1', 'Abby', 10, '2020-01-01'),
	('customer2', 'Bob', 20, '2020-01-15'),
	('customer3', 'Cassey', 5, '2020-01-20'),
	('customer4', 'Dominic', 10, '2020-03-14'),
	('customer5', 'Erica', 20, '2020-04-23'),
	('customer6', 'Francis', 5, '2020-03-12'),
	('customer7', 'George', 10, '2020-02-27'),
	('customer8', 'Henry', 20, '2020-02-18'),
	('customer9', 'Isabel', 5, '2020-03-22'),
	('customer10', 'Jack', 5, '2020-04-12');


CREATE TABLE CreditCard (
	uname varchar(100),
	ccNumber varchar NOT NULL,
	cardType varchar NOT NULL,
	PRIMARY KEY(uname, ccNumber) ,
	FOREIGN KEY(uname) REFERENCES Customer(uname) ON DELETE CASCADE
);

INSERT INTO CreditCard values
	('customer1', '1234567890123456', 'UOB'),
	('customer1', '9248628356938539', 'DBS'),
	('customer2', '2357235758458332', 'Citibank'),
	('customer3', '2423893879348756', 'POSB'),
	('customer4', '2389434923593849', 'DBS'),
	('customer5', '0489732938547000', 'OCBC'),
	('customer6', '9485036470239470', 'POSB'),
	('customer7', '4957985729857348', 'DBS'),
	('customer8', '0495735734859485', 'UOB'),
	('customer9', '4958587598283058', 'POSB'),
	('customer10', '0953870543822548', 'Citibank'); 

CREATE TABLE Orders (
	orderId numeric PRIMARY KEY,
	cuname varchar(100) REFERENCES Customer(uname) ON DELETE CASCADE,
	payment_type varchar NOT NULL,
	deliveryAddress varchar NOT NULL,
	deliveryPostalCode varchar(6) NOT NULL,
	area varchar(20) NOT NULL,
	is_delivered boolean DEFAULT false,
	order_date date,
	order_time time,
	deliveryFee numeric NOT NULL,
	foodCost numeric NOT NULL,
	promoCode varchar
);

INSERT INTO Orders values
	(1,'customer1', 'Cash', 'Blk 123 Serangoon Ave 3 #01-01', '530123','North-East', true, '2020-01-01', '10:52:01', 0,32, 'FREEDELIVERY'),
	(2,'customer1', 'Cash', 'Blk 33 Serangoon Ave 9 #03-02', '538237','North-East', true, '2020-01-01', '13:24:01', 5,8.08, '15OFF'),
	(3,'customer1', 'Credit Card', 'Blk 8 Jurong East 10 #01-01', '600456', 'West', true, '2020-01-01', '17:11:01', 5,7.20, '10OFF'),
	(4,'customer1', 'Credit Card', 'Blk 456 Jurong East 10 #01-01', '600456', 'West', true, '2020-02-01', '16:51:41', 5,38, null),
	(5,'customer1', 'Cash', 'Blk 789 Pasir Ris St 7 #01-01', '520789', 'East', true, '2020-03-01', '17:12:41', 5,30, null),
	(6,'customer1', 'Cash', 'Blk 47 Pasir Ris St 10 #04-23', '520789', 'East', true, '2020-03-06', '12:01:01', 5,11, null),

	(7,'customer2', 'Cash', '3007 Ubi Road 1 02-426', '408701','Central', true, '2020-04-01', '19:01:01', 5,44, null),

	(8,'customer3', 'Credit Card', '20 Ang Mo Kio Industrial Park 2A 02-02', '539215','North-East', true, '2020-04-03', '19:12:29', 5,12, null),

	(9,'customer4', 'Credit Card', 'Blk 221 Bukit Batok East Ave 3 ,12-174', '650221','West', true, '2020-04-04', '12:22:01', 5,15, null),

	(10,'customer5', 'Cash', '521 Bukit Batok Street 23 Excel Building', '659544','West', true, '2020-04-04', '14:01:02', 5,10, null),

	(11,'customer6', 'Credit Card', '1 North Bridge Road, #21-04, High Street Centre', '179094','Central', true, '2020-04-04', '20:32:00', 5,38, null),

	(12,'customer7', 'Cash', '77 High Street 03-05 High Street Plaza', '179433','Central', true, '2020-02-04', '21:23:44', 5,11, null),

	(13,'customer8', 'Cash', '13 Yarrow Gardens', '455018','East', true, '2020-02-23', '15:11:00', 5,6, null),

	(14,'customer9', 'Credit Card', '50 East Coast Road', '429979','East', true, '2020-02-24', '16:00:04', 5,6.4, '20OFF'),

	(15,'customer10', 'Cash', '1 Senoko Crescent', '758283','North', true, '2020-02-25', '10:12:59', 5,11, null),
	(16,'customer10', 'Credit Card', '7 Amoy St Far East Square', '049949','Central', true, '2020-02-25', '19:14:31', 5,15, null); 

CREATE TABLE Reviews (
	orderId numeric REFERENCES Orders(orderId) ON DELETE CASCADE,
	review varchar,
	PRIMARY KEY(orderId)
);

INSERT INTO Reviews values
	(1, 'Very Delicious!!'),
	(2, 'YUMMMZZZ'),
	(5, 'Not as good as I expected'),
	(7, 'so-so'),
	(10, 'Could be better'),
	(13, 'Not bad, would recommend'),
	(15, 'Good food');

CREATE TABLE Contain (
	orderId numeric,
	runame varchar(100),
	fname varchar(100),
    quantity numeric,
	PRIMARY KEY(orderId, runame, fname),
	FOREIGN KEY(orderId) REFERENCES Orders,
	FOREIGN KEY(runame, fname) REFERENCES Food	
);

INSERT INTO Contain values
	(1,'restaurant1', 'Sushi', 1),
	(1,'restaurant1', 'Mochi', 1),
	(1,'restaurant1', 'Ramen', 1),

	(2,'restaurant2', 'Hokkien Mee', 1),
	(2,'restaurant2', 'Prawn Noodles', 1),

	(3,'restaurant3', 'Plain Prata', 3),
	(3,'restaurant3', 'Egg Prata', 2),

	(4,'restaurant4', 'Seafood Aglio Olio', 1),
	(4,'restaurant4', 'Chicken Chop', 1),

	(5,'restaurant5', 'Ribeye Steak', 1),

	(6,'restaurant6', 'Filet O’ Fish', 1),
	(6,'restaurant6', 'Pc Spicy', 1),

	(7,'restaurant7', 'Beef Burger', 2),
	(7,'restaurant7', 'Chocolate Pie', 4),

	(8,'restaurant8', 'Salad Bowl', 1),
	(8,'restaurant8', 'Burrito', 1),

	(9,'restaurant9', 'Kampong Fried Rice', 1),
	(9,'restaurant9', 'Maggie Pataya', 1),
	(9,'restaurant9', 'Butter Chicken', 1),

	(10,'restaurant10', 'Cheese Baked Rice', 1),
	(10,'restaurant10', 'Grilled Chicken', 1),

	(11,'restaurant4', 'Seafood Aglio Olio', 1),
	(11,'restaurant4', 'Chicken Chop', 1), 

	(12,'restaurant6', 'Filet O’ Fish', 1),
	(12,'restaurant6', 'Pc Spicy', 1),

	(13,'restaurant8', 'Salad Bowl', 1),
	(13,'restaurant8', 'Burrito', 1),

	(14,'restaurant3', 'Plain Prata', 3),
	(14,'restaurant3', 'Egg Prata', 2),

	(15,'restaurant6', 'Filet O’ Fish', 1),
	(15,'restaurant6', 'Pc Spicy', 1),

	(16,'restaurant9', 'Kampong Fried Rice', 1),
	(16,'restaurant9', 'Maggie Pataya', 1),
	(16,'restaurant9', 'Butter Chicken', 1);

CREATE TABLE Delivery_Staff (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	dname varchar(100) NOT NULL,
	avg_rating numeric,
	is_delivering boolean default false
);

INSERT INTO Delivery_Staff values
	('parttime1', 'Smith', 4.5),
	('parttime2', 'Alaine', 0),
	('parttime3', 'Carita', 0),
	('parttime4', 'Goober', 4.0),
	('parttime5', 'Michaeline', 0),
	('parttime6', 'Yankee', 0),
	('parttime7', 'James', 0),
	('parttime8', 'Fiona', 0),
	('parttime9', 'Max', 0),
	('parttime10', 'Dylan', 0),
	('fulltime1', 'Grantham', 4.4),
	('fulltime2', 'Denna', 0),
	('fulltime3', 'Rina', 0),
	('fulltime4', 'Harlin', 0),
	('fulltime5', 'Ertha', 0),
	('fulltime6', 'Nola', 3.6),
	('fulltime7', 'Farlie', 0),
	('fulltime8', 'Desmond', 0),
	('fulltime9', 'Lionel', 0),
	('fulltime10', 'Faith', 0),
	('fulltime11', 'Grantham', 2.0),
	('fulltime12', 'Denna', 0),
	('fulltime13', 'Rina', 0),
	('fulltime14', 'Harlin', 0),
	('fulltime15', 'Ertha', 0),
	('fulltime16', 'Nola', 4.0),
	('fulltime17', 'Farlie', 0),
	('fulltime18', 'Desmond', 0),
	('fulltime19', 'Lionel', 0),
	('fulltime20', 'Faith', 0);

CREATE TABLE Delivers ( 
	orderId numeric PRIMARY KEY,
	duname varchar(100) REFERENCES Delivery_Staff(uname), 
	rating numeric,
	depart_restaurant time,
	arrive_restaurant time,
	depart_customer time,
	arrive_customer time,
	FOREIGN KEY(orderId) REFERENCES Orders
);

INSERT INTO Delivers values
	(1,'parttime1', 5.0, '10:53:40', '11:11:11', '11:15:23', '11:30:44'), -- jan 1 wed
	(2,'fulltime1', 4.0, '13:25:33', '13:30:42', '13:32:40', '13:50:20'), -- jan 1 wed 
	(3,'parttime1', 4.0, '17:11:30', '17:20:00', '17:25:00', '17:35:00'), -- jan 1 wed 
	(4,'fulltime1', 5.0, '16:55:00', '17:20:00', '17:25:00', '17:35:00'), -- feb 1 sat 
	(5,'fulltime16', 3.0, '17:15:40', '17:20:00', '17:25:00', '17:35:00'), -- march 1 sun
	(6,'parttime4', 4.0, '12:01:56', '12:10:10', '12:15:58', '12:30:20'), -- march 6 
	(7,'fulltime6', 5.0, '19:03:44', '19:15:15', '19:17:12', '19:33:24'), -- april 1 wed
	(8,'fulltime6', 3.0, '19:12:59', '19:22:23', '19:25:33', '19:55:32'), --april 3 fri
	(9,'fulltime1', 5.0, '12:23:00', '12:34:12', '12:35:00', '12:59:00'), --april 4 sat
	(10,'fulltime1', 4.0, '14:01:59', '14:10:32', '14:12:55', '14:30:22'), --april 4 sat
	(11,'fulltime11', 2.0, '20:32:59', '20:42:58', '20:45:01', '21:02:05'), -- april 4 sat 8pm 
	(12,'fulltime6', 2.0, '21:24:10', '21:30:33', '21:34:56', '21:57:00'), -- feb 4 tues
	(13,'fulltime1', 4.0, '15:11:30', '15:16:30', '15:20:20', '15:40:20'), -- feb 23 sun
	(14,'fulltime16', 5.0, '16:01:00', '16:20:19', '16:22:36', '16:47:38'), -- feb 24 mon shift 1
	(15,'fulltime6', 5.0, '10:13:20', '10:20:33', '10:23:00', '10:43:20'), -- feb 25 tues
	(16,'fulltime6', 3.0, '19:15:20', '19:20:40', '19:22:00', '19:33:41'); -- feb 25 tues shift 4
	
	
CREATE TABLE Part_Time (
	duname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff(uname) ON DELETE CASCADE,
	base_salary numeric default 100,
	flat_rate numeric default 3
);

INSERT INTO Part_Time(duname) values
	('parttime1'),
	('parttime2'), 
	('parttime3'), 
	('parttime4'), 
	('parttime5'), 
	('parttime6'), 
	('parttime7'), 
	('parttime8'), 
	('parttime9'), 
	('parttime10');
	
CREATE TABLE Full_Time (
	duname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff(uname) ON DELETE CASCADE,
	base_salary numeric default 1000,
	flat_rate numeric default 4
);

INSERT INTO Full_Time(duname) values
	('fulltime1'),
	('fulltime2'),
	('fulltime3'),
	('fulltime4'),
	('fulltime5'),
	('fulltime6'),
	('fulltime7'),
	('fulltime8'),
	('fulltime9'),
	('fulltime10'),
	('fulltime11'),
	('fulltime12'),
	('fulltime13'),
	('fulltime14'),
	('fulltime15'),
	('fulltime16'),
	('fulltime17'),
	('fulltime18'),
	('fulltime19'),
	('fulltime20'); 

CREATE TABLE WWS (
	wws_serialNum numeric NOT NULL,
	duname varchar(100) REFERENCES Part_Time ON DELETE CASCADE,
	shift_date date NOT NULL,
	shift_day varchar NOT NULL,
	start_hour time,
	end_hour time,
	PRIMARY KEY (duname, wws_serialNum)
);

INSERT INTO WWS values
	(1,'parttime1', '2020-01-01', 'Wednesday', '10:00:00', '13:00:00'), --3h
	(2,'parttime1', '2020-01-01', 'Wednesday', '14:00:00', '18:00:00'), --4h
	(3,'parttime1', '2020-01-02', 'Thursday', '19:00:00', '23:00:00'), --4h
	(4,'parttime1', '2020-01-03', 'Friday', '10:00:00', '13:00:00'), --3h
	(5,'parttime1', '2020-01-04', 'Saturday', '10:00:00', '13:00:00'), --3h
	(6,'parttime1', '2020-02-12', 'Wednesday', '10:00:00', '14:00:00'), --4h
	(7,'parttime1', '2020-02-13', 'Thursday', '10:00:00', '14:00:00'), --4h
	(8,'parttime1', '2020-02-14', 'Friday', '14:00:00', '18:00:00'), --4h
	(9,'parttime1', '2020-02-15', 'Saturday', '15:00:00', '17:00:00'), --2h
	(10,'parttime1', '2020-02-17', 'Monday', '10:00:00', '14:00:00'), --4h
	(11,'parttime1', '2020-02-17', 'Monday', '15:00:00', '19:00:00'), --4h
	(12,'parttime1', '2020-02-17', 'Monday', '20:00:00', '22:00:00'), --2h

	(1,'parttime2', '2020-02-02', 'Sunday', '10:00:00', '13:00:00'), --3h
	(2,'parttime2', '2020-02-02', 'Sunday', '14:00:00', '18:00:00'), --4h
	(3,'parttime2', '2020-02-02', 'Sunday', '19:00:00', '23:00:00'), --4h
	(4,'parttime2', '2020-02-04', 'Tuesday', '10:00:00', '13:00:00'), --3h
	(5,'parttime2', '2020-02-05', 'Wednesday', '10:00:00', '13:00:00'), --3h
	(6,'parttime2', '2020-02-12', 'Wednesday', '14:00:00', '18:00:00'), --4h
	(7,'parttime2', '2020-02-13', 'Thursday', '10:00:00', '14:00:00'), --4h
	(8,'parttime2', '2020-02-14', 'Friday', '14:00:00', '18:00:00'), --4h
	(9,'parttime2', '2020-03-01', 'Sunday', '15:00:00', '17:00:00'), --2h
	(10,'parttime2', '2020-03-02', 'Monday', '10:00:00', '14:00:00'), --4h
	(11,'parttime2', '2020-03-05', 'Thursday', '15:00:00', '19:00:00'), --4h
	(12,'parttime2', '2020-03-06', 'Friday', '20:00:00', '22:00:00'), --2h

	(1,'parttime3', '2020-02-03', 'Monday', '10:00:00', '13:00:00'), --3h
	(2,'parttime3', '2020-02-03', 'Monday', '14:00:00', '18:00:00'), --4h
	(3,'parttime3', '2020-02-04', 'Tuesday', '16:00:00', '20:00:00'), --4h
	(4,'parttime3', '2020-02-04', 'Tuesday', '21:00:00', '22:00:00'), --1h
	(5,'parttime3', '2020-02-05', 'Wednesday', '10:00:00', '13:00:00'), --3h
	(6,'parttime3', '2020-02-21', 'Friday', '14:00:00', '18:00:00'), --4h
	(7,'parttime3', '2020-02-22', 'Saturday', '10:00:00', '14:00:00'), --4h
	(8,'parttime3', '2020-02-23', 'Sunday', '14:00:00', '18:00:00'), --4h
	(9,'parttime3', '2020-02-24', 'Monday', '15:00:00', '17:00:00'), --2h
	(10,'parttime3', '2020-02-25', 'Tuesday', '10:00:00', '14:00:00'), --4h
	(11,'parttime3', '2020-02-26', 'Wednesday', '15:00:00', '19:00:00'), --4h
	(12,'parttime3', '2020-02-27', 'Thursday', '20:00:00', '22:00:00'), --2h

	(1,'parttime4', '2020-03-02', 'Monday', '10:00:00', '13:00:00'), --3h
	(2,'parttime4', '2020-03-03', 'Tuesday', '10:00:00', '14:00:00'), --4h
	(3,'parttime4', '2020-03-04', 'Wednesday', '19:00:00', '23:00:00'), --4h
	(4,'parttime4', '2020-03-05', 'Thursday', '10:00:00', '13:00:00'), --3h
	(5,'parttime4', '2020-03-06', 'Friday', '10:00:00', '13:00:00'), --3h
	(6,'parttime4', '2020-03-07', 'Saturday', '14:00:00', '18:00:00'), --4h
	(7,'parttime4', '2020-03-08', 'Sunday', '10:00:00', '14:00:00'), --4h
	(8,'parttime4', '2020-03-09', 'Monday', '14:00:00', '18:00:00'), --4h
	(9,'parttime4', '2020-03-10', 'Tuesday', '15:00:00', '17:00:00'), --2h
	(10,'parttime4', '2020-03-11', 'Wednesday', '10:00:00', '14:00:00'), --4h
	(11,'parttime4', '2020-03-12', 'Thursday', '15:00:00', '19:00:00'), --4h
	(12,'parttime4', '2020-03-13', 'Friday', '20:00:00', '22:00:00'), --2h
	
	(1,'parttime5', '2020-03-30', 'Monday', '10:00:00', '13:00:00'), --3h
	(2,'parttime5', '2020-03-30', 'Monday', '14:00:00', '18:00:00'), --4h
	(3,'parttime5', '2020-03-31', 'Tuesday', '10:00:00', '14:00:00'), --4h
	(4,'parttime5', '2020-03-31', 'Tuesday', '15:00:00', '19:00:00'), --4h
	(5,'parttime5', '2020-03-31', 'Tuesday', '20:00:00', '22:00:00'), --2h
	(6,'parttime5', '2020-04-01', 'Wednesday', '10:00:00', '14:00:00'), --4h
	(7,'parttime5', '2020-04-01', 'Wednesday', '15:00:00', '19:00:00'), --4h
	(8,'parttime5', '2020-04-01', 'Wednesday', '20:00:00', '22:00:00'), --2h
	(9,'parttime5', '2020-04-02', 'Thursday', '15:00:00', '17:00:00'), --2h
	(10,'parttime5', '2020-04-02', 'Thursday', '18:00:00', '22:00:00'), --4h
	(11,'parttime5', '2020-04-03', 'Friday', '15:00:00', '19:00:00'), --4h
	(12,'parttime5', '2020-04-03', 'Friday', '20:00:00', '22:00:00'), --2h

	(1,'parttime6', '2020-01-01', 'Wednesday', '10:00:00', '13:00:00'), --3h
	(2,'parttime6', '2020-01-01', 'Wednesday', '14:00:00', '18:00:00'), --4h
	(3,'parttime6', '2020-01-02', 'Thursday', '19:00:00', '23:00:00'), --4h
	(4,'parttime6', '2020-01-03', 'Friday', '10:00:00', '13:00:00'), --3h
	(5,'parttime6', '2020-01-04', 'Saturday', '10:00:00', '13:00:00'), --3h
	(6,'parttime6', '2020-02-12', 'Wednesday', '10:00:00', '14:00:00'), --4h
	(7,'parttime6', '2020-02-13', 'Thursday', '10:00:00', '14:00:00'), --4h
	(8,'parttime6', '2020-02-14', 'Friday', '14:00:00', '18:00:00'), --4h
	(9,'parttime6', '2020-02-15', 'Saturday', '15:00:00', '17:00:00'), --2h
	(10,'parttime6', '2020-02-17', 'Monday', '10:00:00', '14:00:00'), --4h
	(11,'parttime6', '2020-02-17', 'Monday', '15:00:00', '19:00:00'), --4h
	(12,'parttime6', '2020-02-17', 'Monday', '20:00:00', '22:00:00'), --2h

	(1,'parttime7', '2020-02-02', 'Sunday', '10:00:00', '13:00:00'), --3h
	(2,'parttime7', '2020-02-02', 'Sunday', '14:00:00', '18:00:00'), --4h
	(3,'parttime7', '2020-02-02', 'Sunday', '19:00:00', '23:00:00'), --4h
	(4,'parttime7', '2020-02-04', 'Tuesday', '10:00:00', '13:00:00'), --3h
	(5,'parttime7', '2020-02-05', 'Wednesday', '10:00:00', '13:00:00'), --3h
	(6,'parttime7', '2020-02-12', 'Wednesday', '14:00:00', '18:00:00'), --4h
	(7,'parttime7', '2020-02-13', 'Thursday', '10:00:00', '14:00:00'), --4h
	(8,'parttime7', '2020-02-14', 'Friday', '14:00:00', '18:00:00'), --4h
	(9,'parttime7', '2020-03-01', 'Sunday', '15:00:00', '17:00:00'), --2h
	(10,'parttime7', '2020-03-02', 'Monday', '10:00:00', '14:00:00'), --4h
	(11,'parttime7', '2020-03-05', 'Thursday', '15:00:00', '19:00:00'), --4h
	(12,'parttime7', '2020-03-06', 'Friday', '20:00:00', '22:00:00'), --2h

	(1,'parttime8', '2020-02-03', 'Monday', '10:00:00', '13:00:00'), --3h
	(2,'parttime8', '2020-02-03', 'Monday', '14:00:00', '18:00:00'), --4h
	(3,'parttime8', '2020-02-04', 'Tuesday', '16:00:00', '20:00:00'), --4h
	(4,'parttime8', '2020-02-04', 'Tuesday', '21:00:00', '22:00:00'), --1h
	(5,'parttime8', '2020-02-05', 'Wednesday', '10:00:00', '13:00:00'), --3h
	(6,'parttime8', '2020-02-21', 'Friday', '14:00:00', '18:00:00'), --4h
	(7,'parttime8', '2020-02-22', 'Saturday', '10:00:00', '14:00:00'), --4h
	(8,'parttime8', '2020-02-23', 'Sunday', '14:00:00', '18:00:00'), --4h
	(9,'parttime8', '2020-02-24', 'Monday', '15:00:00', '17:00:00'), --2h
	(10,'parttime8', '2020-02-25', 'Tuesday', '10:00:00', '14:00:00'), --4h
	(11,'parttime8', '2020-02-26', 'Wednesday', '15:00:00', '19:00:00'), --4h
	(12,'parttime8', '2020-02-27', 'Thursday', '20:00:00', '22:00:00'), --2h

	(1,'parttime9', '2020-03-02', 'Monday', '10:00:00', '13:00:00'), --3h
	(2,'parttime9', '2020-03-03', 'Tuesday', '10:00:00', '14:00:00'), --4h
	(3,'parttime9', '2020-03-04', 'Wednesday', '19:00:00', '23:00:00'), --4h
	(4,'parttime9', '2020-03-05', 'Thursday', '10:00:00', '13:00:00'), --3h
	(5,'parttime9', '2020-03-06', 'Friday', '10:00:00', '13:00:00'), --3h
	(6,'parttime9', '2020-03-07', 'Saturday', '14:00:00', '18:00:00'), --4h
	(7,'parttime9', '2020-03-08', 'Sunday', '10:00:00', '14:00:00'), --4h
	(8,'parttime9', '2020-03-09', 'Monday', '14:00:00', '18:00:00'), --4h
	(9,'parttime9', '2020-03-10', 'Tuesday', '15:00:00', '17:00:00'), --2h
	(10,'parttime9', '2020-03-11', 'Wednesday', '10:00:00', '14:00:00'), --4h
	(11,'parttime9', '2020-03-12', 'Thursday', '15:00:00', '19:00:00'), --4h
	(12,'parttime9', '2020-03-13', 'Friday', '20:00:00', '22:00:00'), --2h
	
	(1,'parttime10', '2020-03-30', 'Monday', '10:00:00', '13:00:00'), --3h
	(2,'parttime10', '2020-03-30', 'Monday', '14:00:00', '18:00:00'), --4h
	(3,'parttime10', '2020-03-31', 'Tuesday', '10:00:00', '14:00:00'), --4h
	(4,'parttime10', '2020-03-31', 'Tuesday', '15:00:00', '19:00:00'), --4h
	(5,'parttime10', '2020-03-31', 'Tuesday', '20:00:00', '22:00:00'), --2h
	(6,'parttime10', '2020-04-01', 'Wednesday', '10:00:00', '14:00:00'), --4h
	(7,'parttime10', '2020-04-01', 'Wednesday', '15:00:00', '19:00:00'), --4h
	(8,'parttime10', '2020-04-01', 'Wednesday', '20:00:00', '22:00:00'), --2h
	(9,'parttime10', '2020-04-02', 'Thursday', '15:00:00', '17:00:00'), --2h
	(10,'parttime10', '2020-04-02', 'Thursday', '18:00:00', '22:00:00'), --4h
	(11,'parttime10', '2020-04-03', 'Friday', '15:00:00', '19:00:00'), --4h
	(12,'parttime10', '2020-04-03', 'Friday', '20:00:00', '22:00:00'); --2h

CREATE TABLE MWS (
	mws_serialNum numeric NOT NULL,
	duname varchar(100) REFERENCES Full_Time ON DELETE CASCADE,
	work_month varchar NOT NULL,
	day_option numeric NOT NULL,
	shift numeric NOT NULL,
	work_year numeric NOT NULL,
	PRIMARY KEY (duname, mws_serialNum)
);

INSERT INTO MWS values
	(1,'fulltime1', 'January', 1, 1, 2020),
	(1,'fulltime2', 'January', 1, 1, 2020),
	(1,'fulltime3', 'January', 1, 1, 2020),
	(1,'fulltime4', 'January', 1, 1, 2020),
	(1,'fulltime5', 'January', 1, 1, 2020),
	(1,'fulltime6', 'January', 5, 4, 2020),
	(1,'fulltime7', 'January', 5, 4, 2020),
	(1,'fulltime8', 'January', 5, 4, 2020),
	(1,'fulltime9', 'January', 5, 4, 2020),
	(1,'fulltime10', 'January', 5, 4, 2020),
	(1,'fulltime11', 'January', 1, 4, 2020),
	(1,'fulltime12', 'January', 1, 4, 2020),
	(1,'fulltime13', 'January', 1, 4, 2020),
	(1,'fulltime14', 'January', 1, 4, 2020),
	(1,'fulltime15', 'January', 1, 4, 2020),
	(1,'fulltime16', 'January', 5, 1, 2020),
	(1,'fulltime17', 'January', 5, 1, 2020),
	(1,'fulltime18', 'January', 5, 1, 2020),
	(1,'fulltime19', 'January', 5, 1, 2020),
	(1,'fulltime20', 'January', 5, 1, 2020),

	(2,'fulltime1', 'February', 3, 1, 2020),
	(2,'fulltime2', 'February', 3, 1, 2020),
	(2,'fulltime3', 'February', 3, 1, 2020),
	(2,'fulltime4', 'February', 3, 1, 2020),
	(2,'fulltime5', 'February', 3, 1, 2020),
	(2,'fulltime6', 'February', 7, 4, 2020),
	(2,'fulltime7', 'February', 7, 4, 2020),
	(2,'fulltime8', 'February', 7, 4, 2020),
	(2,'fulltime9', 'February', 7, 4, 2020),
	(2,'fulltime10', 'February', 7, 4, 2020),
	(2,'fulltime11', 'February', 3, 4, 2020),
	(2,'fulltime12', 'February', 3, 4, 2020),
	(2,'fulltime13', 'February', 3, 4, 2020),
	(2,'fulltime14', 'February', 3, 4, 2020),
	(2,'fulltime15', 'February', 3, 4, 2020),
	(2,'fulltime16', 'February', 7, 1, 2020),
	(2,'fulltime17', 'February', 7, 1, 2020),
	(2,'fulltime18', 'February', 7, 1, 2020),
	(2,'fulltime19', 'February', 7, 1, 2020),
	(2,'fulltime20','February', 7, 1, 2020),

	(3,'fulltime1', 'March', 2, 1, 2020),
	(3,'fulltime2', 'March', 2, 1, 2020),
	(3,'fulltime3', 'March', 2, 1, 2020),
	(3,'fulltime4', 'March', 2, 1, 2020),
	(3,'fulltime5', 'March', 2, 1, 2020),
	(3,'fulltime6', 'March', 6, 4, 2020),
	(3,'fulltime7', 'March', 6, 4, 2020),
	(3,'fulltime8', 'March', 6, 4, 2020),
	(3,'fulltime9', 'March', 6, 4, 2020),
	(3,'fulltime10', 'March', 6, 4, 2020),
	(3,'fulltime11', 'March', 2, 4, 2020),
	(3,'fulltime12', 'March', 2, 4, 2020),
	(3,'fulltime13', 'March', 2, 4, 2020),
	(3,'fulltime14', 'March', 2, 4, 2020),
	(3,'fulltime15', 'March', 2, 4, 2020),
	(3,'fulltime16', 'March', 6, 1, 2020),
	(3,'fulltime17', 'March', 6, 1, 2020),
	(3,'fulltime18', 'March', 6, 1, 2020),
	(3,'fulltime19', 'March', 6, 1, 2020),
	(3,'fulltime20', 'March', 6, 1, 2020),

	(4,'fulltime1', 'April', 4, 1, 2020),
	(4,'fulltime2', 'April', 4, 1, 2020),
	(4,'fulltime3', 'April', 4, 1, 2020),
	(4,'fulltime4', 'April', 4, 1, 2020),
	(4,'fulltime5', 'April', 4, 1, 2020),
	(4,'fulltime6', 'April', 1, 4, 2020),
	(4,'fulltime7', 'April', 1, 4, 2020),
	(4,'fulltime8', 'April', 1, 4, 2020),
	(4,'fulltime9', 'April', 1, 4, 2020),
	(4,'fulltime10', 'April', 1, 4, 2020),
	(4,'fulltime11', 'April', 4, 4, 2020),
	(4,'fulltime12', 'April', 4, 4, 2020),
	(4,'fulltime13', 'April', 4, 4, 2020),
	(4,'fulltime14', 'April', 4, 4, 2020),
	(4,'fulltime15', 'April', 4, 4, 2020),
	(4,'fulltime16', 'April', 1, 1, 2020),
	(4,'fulltime17', 'April', 1, 1, 2020),
	(4,'fulltime18', 'April', 1, 1, 2020),
	(4,'fulltime19', 'April', 1, 1, 2020),
	(4,'fulltime20', 'April', 1, 1, 2020); 

CREATE TABLE FDS_Manager (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	mname varchar(100) NOT NULL
);

INSERT INTO FDS_Manager values
	('manager', 'Bob'); 

CREATE TABLE FDS_Promo (
	promoId numeric PRIMARY KEY, 
	promoCode varchar, 
	start_date date NOT NULL, 
	end_date date NOT NULL, 
	name varchar,
	muname varchar(100), 
	FOREIGN KEY(muname) REFERENCES FDS_Manager(uname) ON DELETE CASCADE
);

INSERT INTO FDS_Promo values
	(1, '20OFF', '2020-04-01', '2020-05-01', '20% off', 'manager'),
	(2, '50OFF', '2020-01-01', '2020-02-23', '50% off', 'manager'),
	(3, '15OFF', '2020-02-01', '2020-05-01', '15% off', 'manager');