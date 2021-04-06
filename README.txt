How to set up FishRFriends Application:

System Requirements:
1. Docker
2. Wamp Server  & MySQL
3. Python
4. Flask

Steps to set up:
1. Docker-Compose
- Access docker-compose.yml file under /app and edit each microservice image to your docker username.
(e.g image: <docker-username>/payment:1.0)
- In the terminal, change directory to the /app directory, then enter these commands:
	1. docker-compose build
	2. docker-compose up
- After the docker is sucessfully set up, proceed to /app/kong and enter the two same commands.

2.Setting up MySQL
- Start Wamp Server
- Open MySQL workbench or PHPMyAdmin.
- import database.sql and run script
- import sample_data.sql and run script

3. Configuring Kong and RabbitMQ
- RabbitMQ configuration should be automated, but if it is not, then set the following configurations in http://localhost:15672/:
	exchange_name: "confirmed_orders_topic"
	exchange_type: "topic"
	queue_name 1: "Confirmed_Orders_Log"
	binding_key 1:"confirmed.orders"
	queue_name 2: "Payment_Log"
	binding_key 2:"payment.log"

- Kong Configuration:

	1. Proceed to "http://localhost:1337/#!/"dashboard to access konga dashboard, log in using username "admin" and password "adminadmin".
	2. Click on services, and click "add new service"
	3. A total of 5 services will be created. Add these services and the respective routes:
		1. Name: fishapi, url: http://app_fish_1:5000/fish
			-Route 1: Name:get_fish, method:"GET",path:"/fish" 

		2. Name: orderapi, url: http://app_order_1:5002/upcoming_orders
			-Route 1: Name:get_upcoming_orders, method:"GET",path:"/upcoming_orders" 

		3. Name: promotionapi, url: http://app_promotion_1:5004/promotion
			-Route 1: Name:get_all_promotions, method:"GET",path:"/promotion" 
			-Route 2: Name:add_promotion, method:"POST",path:"/promotion" 
			-Route 3: Name:update_promotion, method:"PUT",path:"/promotion" 
			-Route 4: Name:delete_promotion, method:"DELETE",path:"/promotion" 

		4. Name: addfishapi, url: http://app_fish_1:5000/fish/add
			-Route 1: Name:add_fish_stock, method:"PUT",path:"/fish/add" 

		5. Name: updatefishapi, url: http://app_fish_1:5000/deduct
			-Route 1: Name:deduct_fish_stock, method:"PUT",path:"/fish/deduct" 


4. Open a cmd terminal, change directory to "/app", then enter the command "python main.py"
5. Enter "http://localhost:5555" into your browser, and you have successfully set up FishRFriends online platform!

