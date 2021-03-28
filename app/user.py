from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#Fish Microservice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(30), nullable = False, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(30), nullable = False)

    def __init__(self, username, name, password, email):
        self.username = username
        self.name = name
        self.password = password
        self.email = email

    def json(self):
        return {
            "username": self.username, 
            "name": self.name,
            "password" : self.password,
            "email" : self.email
            }




@app.route("/user/<string:username>")
def find_by_username(username):
    user = User.query.filter_by(username = username).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 500,
            "message": "Invalid username"
        }
    ), 500


@app.route("/user", methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(**data)


    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred when adding the user."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(port=5001, debug=True)
