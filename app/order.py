#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
#Change to your own database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/FISH_ORDER'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

#Windows
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fish_order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)  

class FishOrder(db.Model):
    __tablename__ = 'fish_order'

    fish_order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # payment_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def __init__(self, amount, username):
        # self.payment_id =  payment_id
        self.amount = amount
        self.username = username

    def json(self):

        dto = {
            'fish_order_id': self.fish_order_id,
            # 'payment_id': self.payment_id,
            'amount' : self.amount,
            'username' : self.username
        }



        return dto

class FishOrderItem(db.Model):
    __tablename__ = 'fish_order_item'

    fish_id = db.Column(db.Integer, primary_key=True)
    fish_order_id = db.Column(db.ForeignKey(
        'fish_order.fish_order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, fish_id, fish_order_id, quantity, price):
        self.fish_id = fish_id
        self.fish_order_id = fish_order_id
        self.quantity = quantity
        self.price = price

    def json(self):

        dto = {
            'fish_id': self.fish_id,
            'fish_order_id': self.fish_order_id,
            'quantity': self.quantity,
            'price': self.price,
        }


        return dto


@app.route("/order")
def get_all():
    orderlist = FishOrder.query.all()
    if len(orderlist):
        data_json = {
            "code" : 200,
            "data" : {
                "orders": []
            }
        }

        for order in orderlist:
            order = order.json()
            order_items = FishOrderItem.query.filter_by(fish_order_id = order['fish_order_id'])
            order['order_items'] = [item.json() for item in order_items]
            data_json['data']['orders'].append(order)
        return jsonify(data_json)

    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
        ), 404

#working
@app.route("/order/<string:fish_order_id>")
def find_by_order_id(fish_order_id):
    order = FishOrder.query.filter_by(fish_order_id=fish_order_id).first()
    if order:
        order = order.json()
        order_items = FishOrderItem.query.filter_by(fish_order_id = order['fish_order_id'])
        order['order_items'] = [item.json() for item in order_items]
        return jsonify(
            {
                "code": 200,
                "data": order
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "fish_order_id": fish_order_id
            },
            "message": "Order not found."
        }
        ), 404

#We cannot create order yet because no order item

#when using this post method, send in data in json, with each order_item in a json format
# {
#   'order_items' : [{
#                       'fish_id' : 1,
#                       'price' : 10
#                        'quantity' : 5},
#                       {
#                       'fish_id' : 1,
#                       'price' : 10
#                        'quantity' : 5}
# ]
# } 

@app.route("/order", methods=['POST'])
def create_order():
    data =request.get_json()


    order = FishOrder(amount=data['amount'], username=data['username'])
    db.session.add(order)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    order_items = data['order_items']
    fish_order_id = order.fish_order_id

    for item in order_items:
        order_item = FishOrderItem(fish_order_id=fish_order_id, **item)
        db.session.add(order_item)
        

    try:
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201



# @app.route("/order", methods=['POST'])
# def create_order():
#     data =request.get_json()


#     username = request.json.get('username', None)
#     order = fish_order(username=username, status='NEW')

#     cart_item = request.json.get('order_items')
#     for item in cart_item:
#         order.order_item.append(fish_order_item(
#             fish_id=item['fish_id'], quantity=item['quantity']))

#     try:
#         db.session.add(order)
#         db.session.commit()
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred while creating the order. " + str(e)
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": order.json()
#         }
#     ), 201


# We cannot update order item yet cos no order item

# @app.route("/order/<string:fish_order_id>", methods=['PUT'])
# def update_order(fish_order_id):
#     try:
#         order = fish_order.query.filter_by(fish_order_id=fish_order_id).first()
#         if not order:
#             return jsonify(
#                 {
#                     "code": 404,
#                     "data": {
#                         "fish_order_id": fish_order_id
#                     },
#                     "message": "Order not found."
#                 }
#             ), 404

#         # update status
#         data = request.get_json()
#         if data['status']:
#             order.status = data['status']
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": order.json()
#                 }
#             ), 200
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "fish_order_id": fish_order_id
#                 },
#                 "message": "An error occurred while updating the order. " + str(e)
#             }
#         ), 500


if __name__ == '__main__':
    #print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(port=5001, debug=True)
