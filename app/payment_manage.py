from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http
import amqp_setup
import pika
import json

#Payment Management Microservice

app = Flask(__name__)

CORS(app)  

promotion_URL = environ.get('promotion_URL') or "http://localhost:5004/promotion"
fish_order_URL = environ.get('fish_order_URL') or "http://localhost:5002/order"
fish_URL = environ.get('fish_URL') or "http://localhost:5000/fish"
payment_URL = environ.get('payment_URL') or "http://localhost:5003/payment"


@app.route("/payment_manage", methods = ['POST'])
def manage_payment():
   # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order_info = request.get_json()
            # print("\nReceived an order in JSON:", order_info)

            # do the actual work
            # 1. Send order info {cart items}
            result = process_payment(order_info)

            if result['code'] in range (200, 300):
                    payment_json = {
                    "amount" : result['data']['order_info']['amount'],
                    "username" : result['data']['order_info']['username'],
                    "fish_order_id" : result['data']['order_info']['fish_order_id']
                    }
                    payment_json = json.dumps(payment_json)
                    order_info['fish_order_id'] = result['data']['order_info']['fish_order_id']
                    amqp_setup.check_setup()
                    message = json.dumps(order_info)
                    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="confirmed.orders", body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
                    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="payment.log", body=payment_json, properties=pika.BasicProperties(delivery_mode = 2)) 
            return jsonify(result), result['code']

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "payment_manage internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def process_payment(order_info):

    #Update fish quantity
    fish_result = invoke_http(fish_URL + "/deduct", method = 'PUT', json = order_info['order_items'])
    code = fish_result['code']
    print(fish_result)
    #Error in updating fish qty
    if code not in range(200, 300):
        return {
            "code": 501,
            "data": order_info['order_items'],
            "message": "Invalid fish id or insufficient fish qty"
        }    
    #End of fish quantity update

    
    # Add order to database

    fish_order_result = invoke_http(fish_order_URL, method = 'POST', json = order_info)


    if fish_order_result['code'] not in range(200, 300):
        return {
            "code": 504,
            "data" : order_info,
            "message": "Unsuccessful order creation!"
        } 


    # # Add successful payment to payment microservice
    # payment_json = {
    #     "amount" : order_info['amount'],
    #     "username" : order_info['username'],
    #     "fish_order_id" : fish_order_result['data']['fish_order_id']
    # }
   
    # payment_result = invoke_http(payment_URL, method = 'POST', json = payment_json)


    # if payment_result['code'] not in range(200, 300):
    #     return {
    #         "code": 503,
    #         "data" : payment_json,
    #         "message": "Unsuccessful payment!"
    #     }      

    order_info['fish_order_id'] = fish_order_result['data']['fish_order_id']

    return {
        'code' : 201,
        'data' : {
            'order_info': order_info,
        }
        }



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
