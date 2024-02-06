from flask import  render_template, flash, redirect, url_for,request
from jobease import app, db, bcrypt
from jobease import app
from jobease.models import User, JobPost
from jobease.forms import RegistrationForm, LoginForm
from jobease.database import load_jobs_from_db
from flask_login import login_user, current_user, logout_user, login_required


'''jobs = [
    {
        'title': 'Software Engineer',
        'location': 'San Francisco, CA',
        'salary': 100000,
        'currency': 'USD',
        'description': 'Exciting opportunity for a software engineer...',
        'responsibilities': 'Design and implement software solutions...',
    }
]
'''

jobs = load_jobs_from_db()

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' registering users and put them into the database '''
    if current_user.is_authenticated:
        return redirect(url_for('jobs'))    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

 

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('jobs_list'))
        else:
            flash('Log in unsuccessful. Please check email and password!', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='user/upload/profile_picture/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file)