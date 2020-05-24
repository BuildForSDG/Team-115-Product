import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

application = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__)) #base directory (neccessary for setting the database)

class Config(object):
    SECRET_KEY = '656000$5OSx9BjlfgsRiXRQ$KhLmehehK06aWAookDVh' #secret keys for forms and sessions
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') #set the database uri
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True   #enable automatic commit of database changes at the end of each request
    SQLALCHEMY_TRACK_MODIFICATIONS = False #disable signaling the app anytime a database change is made

application.config.from_object(Config)

#Bootstrap(app)
db = SQLAlchemy(application)
db.init_app(application)
migrate = Migrate(application, db)

#Resgister blueprints
from .users import users as users_blueprint
from .solutions import solutions as solutions_blueprint

application.register_blueprint(users_blueprint)
application.register_blueprint(solutions_blueprint)