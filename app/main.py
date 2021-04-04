#we just have to run this to render webpages
from flask import Flask, Blueprint, render_template, jsonify, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import requests
import json



#included the db elemments but have yet to do anything wthem
db= SQLAlchemy()
DB_NAME = "database.db"


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.config['SECRET_KEY'] = 'WELCOMETOFISHCYCLE'
CORS(app, resources=r'http://0.0.0.1/fish/put', headers='Content-Type')


@app.route('/')
def index():
    return render_template('google-sign-in.html')

#we can pass conditionals through to our pages and all
@app.route('/home')
def home():
    try:
        fish = requests.request('GET', 'http://127.0.0.1:5000/fish', json = None)
        data= fish.json()
    except:
        data = {'code': 400, 'data': {'fishes': [{'description': 'Theres no Fish', 'fish_id': 1, 'fishname': 'salmon', 'price': 5.0, 'stock_qty': 100}]}}

    return render_template("home.html", fishes = data['data']['fishes'], datacode = data['code'])

@app.route('/checkout', methods=['GET','POST'])
def paypal():
    result = 0
    data= None
    p_data='Tester'
    discount = 0;

    def try_code(code):
        promotions = requests.request('GET', 'http://127.0.0.1:5004/promotion/'+code, json = None)
        promotions_status = promotions.status_code
        if(promotions_status == 200):
            p_data = promotions.json()
        else:
            p_data =None
        return p_data

    form_data = request.values.get("promotion_code")
    if(form_data != None):
        p_data = try_code(form_data)
        if p_data != None:
            discount = p_data['data']['discount']

    result = request.form
    x = result.to_dict()
    data = json.loads(x['Name'])
    
    return render_template('checkout.html', data=data, p_data =p_data , form_data = form_data ,discount = discount)

@app.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text = "Testing" , username ="Weimin")

@app.route('/logout')
def logout():
    return "<p>Logout</p>"

@app.route('/manage',methods=['GET','PUT'])
def management():
    data_list = []
    try:
        orders = requests.request('GET', 'http://localhost:8000/upcoming_orders', json = None)
        order_status = orders.status_code
        if(order_status == 200):
            order_data = orders.json()
        else:
            order_data=None

        data_list.append(order_data)

        fishes = requests.request('GET', 'http://localhost:8000/fish', json = None)
        fishes_status = fishes.status_code
        if(fishes_status == 200):
            fish_data = fishes.json()
        else:
            fish_data =None

        data_list.append(fish_data)

        promotions = requests.request('GET', 'http://localhost:8000/promotion', json = None)
        promotions_status = promotions.status_code
        if(promotions_status == 200):
            p_data = promotions.json()
        else:
            p_data =None
        
        data_list.append(p_data)

    except:
        data_list=['hello', {}, None]

    return render_template("manage.html", data_list =data_list)

@app.route('/promomod', methods=['GET','POST'])
def promo_mod():
    def generate():
        promotions = requests.request('GET', 'http://127.0.0.1:8000/promotion', json = None)
        promotions_status = promotions.status_code
        if(promotions_status >= 200 and promotions_status <= 300):
            p_data = promotions.json();
            return p_data;
        else:
            p_data =None
            return p_data;

    p_data = generate()
    del_data=request.form.get("delete_promo")
    promo_data = request.form.get("promotion_code")
    dis_data = request.form.get("discount")

    if(del_data != None):
        return_del_data = requests.delete('http://127.0.0.1:8000/promotion/'+ str(del_data))
        p_data = generate()
        flash("Promo Code has been deleted", category='success')
        return render_template("promo.html", p_data=p_data)

    if(promo_data != None):
        send_data ={'promotion_code':promo_data,'discount': dis_data}
        return_send = requests.post('http://127.0.0.1:8000/promotion', json = send_data)
        if(return_send.status_code == 201):
            flash("Promo Code has been added", category='success')
            p_data = generate()
            return render_template("promo.html", p_data=p_data)
        else:
            flash("Promo Code has been added before", category='error')

    return render_template("promo.html", p_data=p_data)


@app.route('/confrim', methods=['GET','POST'])
def confrimation():
    return render_template("confrim.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555,debug=True)