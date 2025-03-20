# Description: This file is the entry point of the application. It initializes the Flask app, the database, the bcrypt, the login manager, the mail, and the logger. It also registers the blueprints of the application.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

from dtp.config import Config
from dtp.log_config import setup_logger

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
mail = Mail(app)

logger = setup_logger()

login_manager = LoginManager(app)
login_manager.login_view = 'students.login'
login_manager.login_message_category = 'info'

from dtp.attendance import attendance
from dtp.auth import auth
from dtp.core import core
from dtp.courses import courses
from dtp.management import management
from dtp.profile import profile 

app.register_blueprint(attendance)
app.register_blueprint(auth)
app.register_blueprint(core)
app.register_blueprint(courses)
app.register_blueprint(management)
app.register_blueprint(profile)

from dtp.models import AttendanceRecord, Course, Student, University, Faculty, Department, Class