#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

import amqp_setup

monitorBindingKey='confirmed.orders'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Confirmed_Orders_Log' 
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print(order)
    print("processing confirmed order....")
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "fishrfriendst3@gmail.com"
    password = "Fishrfriendst3!"
    receiver_email = order['username']
    message = MIMEMultipart("alternative")
    message["Subject"] = "Order Confirmation: #" + str(order['fish_order_id']) 
    message["From"] = sender_email
    message["To"] = receiver_email

    order_items = ""
    for item in order['order_items']:
        order_items += "<tr><td>" + item['fish_id'] + "</td><td>" + str(item['quantity']) + "</td></tr>"

    html = """\
    <html>
    <body>
        <p> 
            Thank you for purchasing from FishRFriends! <br><br>

            Here are your order details: <br>

            <b>Collection Date and Time: {collection_datetime}</b>
        </p>
        <table border = '1px'>
            <tr>
                <th>Order Item</th>
                <th>Quantity</th>
            </tr>
            {order_items}
        </table>

        <p><b>Total Amount: ${amount}</b></p>

        <p>
            FishRFriends Pte Ltd <br>
            Contact us at: <br>
            42 Wallaby Way, Sydney <br>
            PH: 9123 4567 
        </p>
    </body>
    </html>
    """.format(collection_datetime=order['collection_datetime'], order_items=order_items, amount=str(order['amount']))
    message.attach(MIMEText(html, "html")) 

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
