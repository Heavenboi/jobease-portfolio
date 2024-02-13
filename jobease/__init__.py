from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '6eef104ab11c0cb779c74b3690ff613a'

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nigel:Heavenboi20@localhost/jobease'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)

# Import routes after initializing extensions to avoid circular imports
from jobease import routes
