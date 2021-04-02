#login logout signup

from flask import Blueprint, render_template, request, flash, jsonify
import requests

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text = "Testing" , username ="Weimin")


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

    
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1  = request.form.get('password1')
        password2  = request.form.get('password2')
        #requirements here
        if password1 == password2 :
        #message flashing
            flash("Passwords do not match", category='error')
            pass
        else:
            flash('Account has been created!', category='success')
            #add to database

    return render_template("signup.html")


@auth.route('/manage',methods=['GET'])
def management():
    orders = requests.request('GET', 'http://127.0.0.1:5002/order', json = None)
    order_status = orders.status_code
    if(order_status == 200):
        data = orders.json()
    else:
        data= None

    fishes = requests.request('GET', 'http://127.0.0.1:5000/fish', json = None)
    fishes_status = fishes.status_code
    if(fishes_status == 200):
        fish_data = fishes.json()
    else:
        fish_data =None

    promotions = requests.request('GET', 'http://127.0.0.1:5004/promotion', json = None)
    promotions_status = promotions.status_code
    if(promotions_status == 200):
        p_data = promotions.json()
    else:
        p_data =None


    return render_template("manage.html",orders_data = data, code = order_status , fish_data =fish_data, fish_code = fishes_status, p_data = p_data)

@auth.route('/promomod', methods=['GET','POST'])
def promo_mod():

    def generate():
        promotions = requests.request('GET', 'http://127.0.0.1:5004/promotion', json = None)
        promotions_status = promotions.status_code
        if(promotions_status == 200):
            p_data = promotions.json()
        else:
            p_data =None
        return p_data

    p_data = generate()

    del_data=request.form.get("delete_promo")
    print(del_data)
    promo_data = request.form.get("promotion_code")
    print(promo_data)
    dis_data = request.form.get("discount")
    print(dis_data)
    if(del_data != None):
        return_del_data = requests.delete('http://127.0.0.1:5004/promotion/'+ str(del_data))
        print(return_del_data.text)
        p_data = generate()
        return render_template("promo.html", p_data=p_data)

    if(promo_data != None):
        send_data ={'promotion_code':promo_data,'discount': dis_data}
        return_send = requests.post('http://127.0.0.1:5004/promotion', json = send_data)
        if(return_send.status_code == 201):
            flash("Promo Code has been added", category='success')
            p_data = generate()
            return render_template("promo.html", p_data=p_data)
        else:
            flash("Promo Code has been added before", category='error')

    return render_template("promo.html", p_data=p_data)