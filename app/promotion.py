from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ

#Fish Microservice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/promotion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Promotion(db.Model):
    __tablename__ = 'promotion'

    promotion_code = db.Column(db.Integer, primary_key=True)
    discount = db.Column(db.Integer, nullable = False)

    def __init__(self, promotion_code, discount):
        self.promotion_code = promotion_code
        self.discount = discount

    def json(self):
        return {"promotion_code": self.promotion_code, "discount": self.discount}

@app.route("/promotion")
def get_all():
    promotionlist = Promotion.query.all()
    if len(promotionlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "promotions": [promotion.json() for promotion in promotionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no promotions available."
        }
    ), 404


@app.route("/promotion/<string:promotion_code>")
def find_by_promotion_code(promotion_code):
    promotion_code = Promotion.query.filter_by(promotion_code=promotion_code).first()
    if promotion_code:
        return jsonify(
            {
                "code": 200,
                "data": promotion_code.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Invalid promotion code!"
        }
    ), 500


@app.route("/promotion", methods=['POST'])
def create_promotion():
    data = request.get_json()
    promotion = Promotion(**data)

    try:
        db.session.add(promotion)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 405,
                "data": data,
                "message": "An error occurred creating the promotion."
            }
        ), 405

    return jsonify(
        {
            "code": 201,
            "data": promotion.json()
        }
    ), 201


@app.route("/promotion", methods=['PUT'])
def update_promotion():
    data = request.get_json()
    promotion = Promotion.query.filter_by(promotion_code=data['promotion_code']).first()
    if promotion:
        promotion.discount = data['discount'] 
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": promotion.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "promotion_code": data['promotion_code']
            },
            "message": "Promotion not found."
        }
    ), 404


@app.route("/promotion/<string:promotion_code>", methods=['DELETE'])
def delete_promotion(promotion_code):
    promotion = Promotion.query.filter_by(promotion_code=promotion_code).first()
    if promotion:
        db.session.delete(promotion)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "promotion_code": promotion_code
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "promotion_code": promotion_code
            },
            "message": "Promotion code not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
