from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Config:
    UPLOAD_FOLDER = 'static/user/upload/profile_picture'
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kq489gxwrraoohqo9a61:pscale_pw_lnC7G73UBbPN0CLeUtDDLeluSpAEhmARGb6wubQz18d@aws.connect.psdb.cloud/jobease-database?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '6eef104ab11c0cb779c74b3690ff613a'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db = SQLAlchemy(app)
