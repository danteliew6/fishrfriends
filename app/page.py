#Where users can navigate to
#this file will have the URLS inside of it
from flask import Blueprint, render_template, jsonify
import requests
from flask import request
import json

page = Blueprint('page', __name__)


@page.route('/')
def index():
    return render_template('google-sign-in.html')


#we can pass conditionals through to our pages and all
@page.route('/home')
def home():
    try:
        fish = requests.request('GET', 'http://127.0.0.1:5000/fish', json = None)
        data= fish.json()
    except:
        data = {'code': 400, 'data': {'fishes': [{'description': 'Theres no Fish', 'fish_id': 1, 'fishname': 'salmon', 'price': 5.0, 'stock_qty': 100}]}}

    return render_template("home.html", fishes = data['data']['fishes'], datacode = data['code'])

@page.route('/checkout', methods=['GET','POST'])
def paypal():
    result = 0
    if request.method == 'POST':
        result = request.form
        #print(type(result))
        #print(jsonify(result))
        #print(result['Name'])
        #print(jsonify(result['Name']))
        x = result.to_dict()
        print(x)
        print(type(x))

    print(type(x['Name']))
    print(jsonify(x['Name']))
    data = json.loads(x['Name'])
    print(type(data['price']))
    print(type(data['orders']))
    print(type(data['orders'][0]))


    return render_template('checkout.html', data=data)



