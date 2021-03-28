USE PAYMENT;

insert into payment(username, amount, fish_order_id) VALUES ('dante',100,1);
insert into payment(username, amount, fish_order_id) VALUES ('daaaa',40,5);
insert into payment(username, amount, fish_order_id) VALUES ('tom',150,5);
insert into payment(username, amount, fish_order_id) VALUES ('cat',130,1);
insert into payment(username, amount, fish_order_id) VALUES ('tan',10,1);


USE FISH;

insert into fish(fishname, stock_qty, description) VALUES ('salmon', 100, 'everyone's fav fish!');
insert into fish(fishname, stock_qty, description) VALUES ('dory', 100, 'finding dory!');
insert into fish(fishname, stock_qty, description) VALUES ('nemo', 100, 'clown!!');
insert into fish(fishname, stock_qty, description) VALUES ('shark', 100, 'fish not food!');

USE PROMOTION;
insert into promotion(promotion_code, discount) VALUES ('fishrfriends', 10);
insert into promotion(promotion_code, discount) VALUES ('findingdory', 20);
insert into promotion(promotion_code, discount) VALUES ('fish2021', 30);
insert into promotion(promotion_code, discount) VALUES ('ilovefish', 15);


USE FISH_ORDER;
insert into fish_order(payment_id, quantity, amount) VALUES (1, 20, 50);
insert into fish_order(payment_id, quantity, amount) VALUES (4, 10, 40);
insert into fish_order(payment_id, quantity, amount) VALUES (2, 10, 30);

insert into fish_order_item() VALUES ();