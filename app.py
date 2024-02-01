from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '6eef104ab11c0cb779c74b3690ff613a'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#db = SQLAlchemy(app)



jobs = [{
    'title': 'Frontend developer',
    'salary': '15200/year',
    'type': 'Full-Time',
    'location': 'Los Vegas. USA'
},
{
    'title': 'Backend developer',
    'salary': '22200/year',
    'type': 'Full-Time',
    'location': 'Johannesburg, SA'
},
{

    'title': 'Product designer',
    'salary': '12900/year',
    'type': 'Full-Time',
    'location': 'Zimabawe. USA'
},
{
    'title': 'Frontend developer',
    'salary': '15200/year',
    'type': 'Full-Time',
    'location': 'Toronto. Canada'
}]

@app.route("/")
def homepage():
    return render_template('home.html', jobs=jobs)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/jobs")
def jobs_list():
    return render_template('jobs.html', jobs=jobs)

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('jobs_list'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'wooden@gmail.com' and form.password.data == 'password':
            flash('You have logged in', 'success')
            return redirect(url_for('jobs_list'))
        else:
            flash('Log in unsuccessful. Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

