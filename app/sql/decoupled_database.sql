SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+08:00";


drop schema if exists USER;
CREATE SCHEMA USER;
USE USER;

-- --------------------------------------------------------

--
-- Table structure for table "user"
--

DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS user (
  username varchar(30) NOT NULL,
  name varchar(30) NOT NULL,
  password varchar(100) NOT NULL,
  email varchar(30) NOT NULL,
  CONSTRAINT user_pk PRIMARY KEY (username)
)ENGINE=InnoDB DEFAULT CHARSET=utf8; 


drop schema if exists PAYMENT;
CREATE SCHEMA PAYMENT;
USE PAYMENT;

--
-- Table structure for table "payment"
--

DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
  username varchar(30) NOT NULL,
  amount int NOT NULL,
  fish_order_id int NOT NULL,
  datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT payment_pk PRIMARY KEY (username, fish_order_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; 



drop schema if exists FISH;
CREATE SCHEMA FISH;
USE FISH;


--
-- Table structure for table "fish"
--

DROP TABLE IF EXISTS fish;
CREATE TABLE fish (
  fish_id int NOT NULL AUTO_INCREMENT,
  fishname varchar(30) NOT NULL,
  price float NOT NULL,
  stock_qty int NOT NULL CHECK (stock_qty >= 0),
  description varchar(100) NOT NULL,
  CONSTRAINT fish_pk PRIMARY KEY (fish_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; 


drop schema if exists FISH_ORDER;
CREATE SCHEMA FISH_ORDER;
USE FISH_ORDER;


--
-- Table structure for table "fish_order"
--


DROP TABLE IF EXISTS fish_order;

CREATE TABLE fish_order (
  fish_order_id int NOT NULL AUTO_INCREMENT,
  username varchar(100) NOT NULL,
  amount FLOAT NOT NULL,
  collection_datetime DATETIME NOT NULL,
  CONSTRAINT fish_order_pk PRIMARY KEY (fish_order_id)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; 

DROP TABLE IF EXISTS fish_order_item;

CREATE TABLE fish_order_item (
  fish_id int NOT NULL,
  fish_order_id int NOT NULL,
  quantity int NOT NULL,
  price float NOT NULL,
  CONSTRAINT fish_order_item_pk PRIMARY KEY(fish_id, fish_order_id),
  CONSTRAINT fish_order_item_fk1 FOREIGN KEY (fish_order_id) REFERENCES fish_order(fish_order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



drop schema if exists PROMOTION;
CREATE SCHEMA PROMOTION;
USE PROMOTION;

--
-- Table structure for table "promotion"
--

DROP TABLE IF EXISTS promotion;
CREATE TABLE promotion (
  promotion_code VARCHAR(30) NOT NULL,
  discount int NOT NULL,
  CONSTRAINT promotion_pk PRIMARY KEY (promotion_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8; 


