SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+08:00";


drop schema if exists fishrfriends;
CREATE SCHEMA fishrfriends;
USE fishrfriends;

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



--
-- Table structure for table "payment"
--

DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
  payment_id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(30) NOT NULL,
  amount int(6) NOT NULL,
  datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT payment_pk PRIMARY KEY (payment_id),
  CONSTRAINT payment_fk FOREIGN KEY (username) references user(username)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; 

--
-- Table structure for table "fish"
--

DROP TABLE IF EXISTS fish;
CREATE TABLE fish (
  fish_id int(11) NOT NULL AUTO_INCREMENT,
  fishname varchar(30) NOT NULL,
  stock_qty int(6) NOT NULL,
  description varchar(100) NOT NULL,
  CONSTRAINT fish_pk PRIMARY KEY (fish_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; 


--
-- Table structure for table "fish_order"
--


DROP TABLE IF EXISTS fish_order;

CREATE TABLE fish_order (
  fish_order_id int(11) NOT NULL AUTO_INCREMENT,
  fish_id int(11) NOT NULL,
  payment_id int(11) NOT NULL,
  quantity int(6) NOT NULL,
  CONSTRAINT fish_order_pk PRIMARY KEY (fish_order_id),
  CONSTRAINT fish_order_fk1 FOREIGN KEY (fish_id) references fish(fish_id),
  CONSTRAINT fish_order_fk2 FOREIGN KEY (payment_id) references payment(payment_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8; 

--
-- Table structure for table "promotion"
--

DROP TABLE IF EXISTS promotion;
CREATE TABLE promotion (
  promotion_code VARCHAR(30) NOT NULL,
  discount int(2) NOT NULL,
  CONSTRAINT promotion_pk PRIMARY KEY (promotion_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8; 


