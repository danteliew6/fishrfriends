from flask import Flask ,render_template

app =Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/test")
def index():
    return render_template('new.html')

@app.route("/pay")
def payment():
    return render_template('checkout.html')

    
if __name__ == '__main__':
    app.run(port=5888, debug=True)





