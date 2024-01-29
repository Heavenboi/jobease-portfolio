from flask import Flask, render_template
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = '6eef104ab11c0cb779c74b3690ff613a'

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'Register', form = 'Form')

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form = 'Form')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)