from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func
from os import environ
import amqp_setup
import json

#Payment Microservice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/payment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  
monitorBindingKey='payment.log'
class Payment(db.Model):
    __tablename__ = 'payment'

    username = db.Column(db.String(30), nullable = False, primary_key = True)
    amount = db.Column(db.Integer, nullable = False)
    fish_order_id = db.Column(db.Integer, nullable = False, primary_key = True)
    datetime = db.Column(db.DateTime, nullable = True, default=func.now())

    def __init__(self, username, amount, fish_order_id):
        self.username = username
        self.amount = amount
        self.fish_order_id = fish_order_id

    def json(self):
        return {
            "username": self.username,
            "amount" : self.amount,
            "fish_order_id" : self.fish_order_id,
            "datetime" : self.datetime
            }

@app.route("/payment")
def get_all():
    payment_list = Payment.query.all()
    if len(payment_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payments": [payment.json() for payment in payment_list]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments yet."
        }
    ), 404


@app.route("/payment/user/<string:username>")
def find_payments_by_username(username):
    payment_list = Payment.query.filter_by(username = username)
    if payment_list:
        return jsonify(
            {
                "code": 200,
                "data": [payment.json() for payment in payment_list]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": username + " has not made any payments yet."
        }
    ), 404

@app.route("/payment/<string:fish_order_id>")
def find_payments_by_order_id(fish_order_id):
    payment = Payment.query.filter_by(fish_order_id = fish_order_id).first()
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Invalid order id."
        }
    ), 404



# @app.route("/payment", methods=['POST'])
# def add_payment():
#     data = request.get_json()
#     payment = Payment(**data)

#     try:
#         db.session.add(payment)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred when adding the payment."
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": payment.json()
#         }
#     ), 201




def receivePaymentLog():
    amqp_setup.check_setup()
        
    queue_name = 'Payment_Log' 
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processPaymentLog(json.loads(body))
    print() # print a new line feed

def processPaymentLog(payment):
    print("logging payment transaction....")
    payment_data = Payment(**payment)

    try:
        db.session.add(payment_data)
        db.session.commit()
    except:
        print("error committing payment log to database")

  

if __name__ == '__main__':
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receivePaymentLog()
    app.run(host='0.0.0.0', port=5003, debug=True)
    
    
