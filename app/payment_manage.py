from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

#Payment Management Microservice

app = Flask(__name__)

CORS(app)  

promotion_URL = environ.get('promotion_URL') or "http://localhost:5004/promotion"
fish_order_URL = environ.get('fish_order_URL') or "http://localhost:5002/order"
fish_URL = environ.get('fish_URL') or "http://localhost:5000/fish"
user_URL = environ.get('user_URL') or "http://localhost:5001/user"
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
            # print(result)

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
    # Validate promotion code
    # promotion_code_result = invoke_http(promotion_URL + "?promotion_code" + order_info['promotion_code'], method='GET', json=None)
    # code = promotion_code_result['code']

    # # Return invalid promotion code
    # if code not in range(200, 300):
    #     return {
    #         "code": 500,
    #         "data": {"promotion_code_result": promotion_code_result},
    #         "message": "Invalid promotion code or promotion code error."
    #     }
    # # End of promotion code validation


    #Update fish quantity
    fish_result = invoke_http(fish_URL, method = 'PUT', json = order_info['order_items'])
    code = fish_result['code']

    #Error in updating fish qty
    if code not in range(200, 300):
        return {
            "code": 501,
            "data": order_info['order_items'],
            "message": "Invalid fish id or insufficient fish qty"
        }    
    #End of fish quantity update


    # STRIPE API IMPLEMENTATION HERE
    # Hardcoding success code and payment id here first
    stripe_response_json = {
        'payment_status' : 201
    }

    if stripe_response_json['payment_status'] not in range(200,300):
        return {
            "code": 502,
            "payment_result": "Unsuccessful transaction!",
            "message": "Denied payment by stripe service."
        }          
    
    # Add order to database

    fish_order_result = invoke_http(fish_order_URL, method = 'POST', json = order_info)

    # print(fish_order_result)

    if fish_order_result['code'] not in range(200, 300):
        return {
            "code": 504,
            "data" : order_info,
            "message": "Unsuccessful order creation!"
        } 


    # Add successful payment to payment microservice
    payment_json = {
        "amount" : order_info['amount'],
        "username" : order_info['username'],
        "fish_order_id" : fish_order_result['data']['fish_order_id']
    }
   
    payment_result = invoke_http(payment_URL, method = 'POST', json = payment_json)


    if payment_result['code'] not in range(200, 300):
        return {
            "code": 503,
            "data" : payment_json,
            "message": "Unsuccessful payment!"
        }      
    # END OF STRIPE API IMPLEMENTATION


    return {
        'code' : 201,
        'data' : {
            'order_info': order_info,
        }
        }



if __name__ == '__main__':
    app.run(port=5005, debug=True)
