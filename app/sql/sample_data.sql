USE PAYMENT;

insert into payment(username, amount, fish_order_id) VALUES ('dante',100,1);
insert into payment(username, amount, fish_order_id) VALUES ('daaaa',40,5);
insert into payment(username, amount, fish_order_id) VALUES ('tom',150,5);
insert into payment(username, amount, fish_order_id) VALUES ('cat',130,1);
insert into payment(username, amount, fish_order_id) VALUES ('tan',10,1);


USE FISH;

insert into fish(fishname, price, stock_qty,  description) VALUES ('salmon', 5, 100, 'everyones fav fish!');
insert into fish(fishname, price, stock_qty, description) VALUES ('dory', 6, 100, 'finding dory!');
insert into fish(fishname, price, stock_qty, description) VALUES ('nemo', 1, 100, 'clown!!');
insert into fish(fishname, price, stock_qty, description) VALUES ('shark', 10, 100, 'fish not food!');

USE PROMOTION;
insert into promotion(promotion_code, discount) VALUES ('fishrfriends', 10);
insert into promotion(promotion_code, discount) VALUES ('findingdory', 20);
insert into promotion(promotion_code, discount) VALUES ('fish2021', 30);
insert into promotion(promotion_code, discount) VALUES ('ilovefish', 15);


USE FISH_ORDER;
insert into fish_order(amount, username, collection_datetime) VALUES (50, 'dante', '2021-05-01');
insert into fish_order(amount, username, collection_datetime) VALUES (40, 'danteliew6', '2021-06-01');
insert into fish_order(amount, username, collection_datetime) VALUES (30, 'fishy', '2021-04-11');

insert into fish_order_item VALUES (5, 1, 5, 5);
insert into fish_order_item VALUES (4, 2, 6, 5); 
insert into fish_order_item VALUES (1, 2, 10, 1);
insert into fish_order_item VALUES (2, 3, 10, 3);
insert into fish_order_item VALUES (1, 1, 25, 1);


