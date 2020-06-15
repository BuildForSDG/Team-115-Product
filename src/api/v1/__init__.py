import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

application = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))  # set db base directory
project_dir = os.path.expanduser('~/team-115-product')
load_dotenv(os.path.join(project_dir, '.env'))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')  # secret keys for forms & sessions
    # set the database uri
    SQLALCHEMY_DATABASE_URI = process.env.DATABASE_URL #os.environ['DATABASE_URL']
    # enable automatic commit of database changes at the end of each request
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # disable signaling the app anytime a database change is made
    SQLALCHEMY_TRACK_MODIFICATIONS = False


application.config.from_object(Config)

# Bootstrap(app)
db = SQLAlchemy(application)
db.init_app(application)
migrate = Migrate(application, db)

# Resgister blueprints
from .users import users as users_blueprint
from .solutions import solutions as solutions_blueprint

application.register_blueprint(users_blueprint)
application.register_blueprint(solutions_blueprint)
