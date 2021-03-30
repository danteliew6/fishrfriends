#Where users can navigate to
#this file will have the URLS inside of it
from flask import Blueprint, render_template
import requests


page = Blueprint('page', __name__)


#we can pass conditionals through to our pages and all
@page.route('/')
def home():
    fish = requests.request('GET', 'http://127.0.0.1:5000/fish', json = None)
    return render_template("home.html", condition = fish.json())

@page.route('/checkout')
def paypal():
    return render_template('checkout.html', FinalValue='123', password="1234")
  


