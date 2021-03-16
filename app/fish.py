from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


#Fish Microservice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/fishrfriends'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Fish(db.Model):
    __tablename__ = 'fish'

    fish_id = db.Column(db.Integer, primary_key=True)
    fishname = db.Column(db.String(64), nullable=False)
    stock_qty = db.Column(db.Integer)
    description = db.Column(db.String(64), nullable=False)

    def __init__(self, fish_id, fishname, stock_qty, description):
        self.fish_id = fish_id
        self.fishname = fishname
        self.stock_qty = stock_qty
        self.description = description

    def json(self):
        return {
            "fish_id": self.fish_id, 
            "fishname": self.fishname, 
            "stock_qty": self.stock_qty, 
            "description": self.description}


@app.route("/fish")
def get_all():
    fishlist = Fish.query.all()
    if len(fishlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "fishes": [fish.json() for fish in fishlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no fishes available."
        }
    ), 404


@app.route("/fish/<string:fish_id>")
def find_by_fish_id(fish_id):
    fish = Fish.query.filter_by(fish_id=fish_id).first()
    if fish:
        return jsonify(
            {
                "code": 200,
                "data": fish.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Fish not found."
        }
    ), 404


@app.route("/fish/<string:fish_id>", methods=['POST'])
def create_fish(fish_id):
    if (Fish.query.filter_by(fish_id=fish_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "fish_id": fish_id
                },
                "message": "Fish already exists."
            }
        ), 400

    data = request.get_json()
    fish = Fish(fish_id, **data)

    try:
        db.session.add(fish)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fish_id": fish_id
                },
                "message": "An error occurred creating the fish."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": fish.json()
        }
    ), 201


@app.route("/fish/<string:fish_id>", methods=['PUT'])
def update_fish(fish_id):
    fish = Fish.query.filter_by(fish_id=fish_id).first()
    if fish:
        data = request.get_json()
        if data['fishname']:
            fish.fishname = data['fishname']
        if data['stock_qty']:
            fish.stock_qty = data['stock_qty']
        if data['description']:
            fish.description = data['description'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": fish.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "fish_id": fish_id
            },
            "message": "Fish not found."
        }
    ), 404


@app.route("/fish/<string:fish_id>", methods=['DELETE'])
def delete_fish(fish_id):
    fish = Fish.query.filter_by(fish_id=fish_id).first()
    if fish:
        db.session.delete(fish)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "fish_id": fish_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "fish_id": fish_id
            },
            "message": "Fish not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
