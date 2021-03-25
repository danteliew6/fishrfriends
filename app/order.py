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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/FISH_ORDER'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)  

class fish_order(db.Model):
    __tablename__ = 'fish_order'

    fish_order_id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, fish_order_id, payment_id):
        self.fish_order_id = fish_id
        self.payment_id =  payment_id

    def json(self):

        dto = {
            'fish_order_id': self.fish_order_id,
            'payment_id': self.payment_id,
        }

        # dto['order_item'] = []
        # for oi in self.order_item:
        #     dto['order_item'].append(oi.json())

        return dto

class fish_order_item(db.Model):
    __tablename__ = 'fish_order_item'

    fish_order_id = db.Column(db.Integer, primary_key=True)
    fish_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, fish_order_id, fish_id, payment_id, quantity):
        self.fish_order_id = fish_id
        self.fish_id = fish_id
        self.quantity = quantity
        self.price = price

    def json(self):

        dto = {
            'fish_order_id': self.fish_order_id,
            'fish_id': self.fish_id,
            'quantity': self.quantity,
            'price': self.price,
        }

        # dto['order_item'] = []
        # for oi in self.order_item:
        #     dto['order_item'].append(oi.json())

        return dto

#We have no order item yet, following DB below is orderitem DB

# class Order_Item(db.Model):
#     __tablename__ = 'order_item'

#     item_id = db.Column(db.Integer, primary_key=True)
#     fish_order_id = db.Column(db.ForeignKey(
#         'order.fish_order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

#     fish_id = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)

#     # fish_order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
#     # order = db.relationship('Order', backref='order_item')
#     order = db.relationship(
#         'Order', primaryjoin='Order_Item.order_id == Order.order_id', backref='order_item')

#     def json(self):
#         return {'item_id': self.item_id, 'fish_id': self.fish_id, 'quantity': self.quantity, 'fish_order_id': self.fish_order_id}

#working
@app.route("/order")
def get_all():
    orderlist = fish_order.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404

#working
@app.route("/order/<string:fish_order_id>")
def find_by_order_id(fish_order_id):
    order = fish_order.query.filter_by(fish_order_id=fish_order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
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

# @app.route("/order", methods=['POST'])
# def create_order():
#     username = request.json.get('username', None)
#     order = fish_order(username=username, status='NEW')

#     cart_item = request.json.get('cart_item')
#     for item in cart_item:
#         order.order_item.append(Order_Item(
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
