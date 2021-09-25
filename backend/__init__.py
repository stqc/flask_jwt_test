from flask import Flask
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
path = os.path.dirname(__file__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(os.path.abspath(path),'testdb.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('jwtname') #Secret key for jwt manager
app.config['JWT_TOKEN_LOCATION']=["cookies"]#how to accept the jwt tokens ['cookies','header','query'] default is header
app.config['JWT_COOKIE_SECURE']=False # should be true in production 
db = SQLAlchemy(app=app)
jwt  = JWTManager(app)
Migrate(app=app,db=db)
