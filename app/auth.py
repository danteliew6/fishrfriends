#login logout signup

from flask import Blueprint, render_template, request, flash

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