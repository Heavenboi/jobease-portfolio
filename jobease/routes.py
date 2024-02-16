import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for,request
from jobease import app, db, bcrypt
from jobease import app
from jobease.models import User, JobPost
from jobease.forms import RegistrationForm, LoginForm, updateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def homepage():
    jobs = JobPost.query.all()
    return render_template('home.html', jobs=jobs)

@app.route("/about")
def about():
    return render_template('about_us.html')

@app.route("/jobs")
def jobs_list():
    jobs = JobPost.query.all()
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
        return redirect(url_for('homepage'))
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/user/upload/profile_picture', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = updateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account is updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='user/upload/profile_picture/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file,form=form)

# Route for creating a new job post
@app.route("/jobs/new", methods=['GET', 'POST'])
@login_required
def new_jobs():
    form = PostForm()
    if form.validate_on_submit():
        job_post = JobPost(title=form.title.data,
                           description=form.description.data,
                           location=form.location.data,
                           salary=form.salary.data,
                           responsibilities=form.responsibilities.data,
                           author=current_user)
        db.session.add(job_post)
        db.session.commit()
        flash('Your job has been created!', 'success')
        return redirect(url_for('homepage'))
    return render_template('create_jobs.html', title='New Job', form=form)
