#creates the database
from flask import Flask #import everything
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from app.middleware import PrefixMiddleware

application = Flask(__name__) 
application.config.from_object(Config) #load the database config using class Config defined in config.py
db = SQLAlchemy(application) #defines dba as an object of SQlalchemy
migrate = Migrate(application, db) #used to migrate the database
login = LoginManager(application) #route the url here
login.login_view = 'login' #directs the url and route to login() in routes.py
bootstrap = Bootstrap5(application) #put css

# set voc=False if you run on local computer
#RMB TO CHANGE LATER
application.wsgi_app = PrefixMiddleware(application.wsgi_app, voc=False) #Sets the url


from app import routes, models #import your routes for ur different url
