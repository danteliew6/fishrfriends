#Where users can navigate to
#this file will have the URLS inside of it
from flask import Blueprint, render_template

page = Blueprint('page', __name__)


#we can pass conditionals through to our pages and all
@page.route('/')
def home():
    return render_template("home.html", condition = True)

@page.route('/checkout')
def paypal():
    return render_template('checkout.html', username="weimin", password="1234")
  


