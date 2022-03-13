from flask import Flask
from flask_cors import CORS
import os

from flask_mysqldb import MySQL
mysql = MySQL()

from .db.routes import db
from .register.routes import register
from .login.routes import login

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
    
    global mysql 
    mysql = MySQL(app)
    app.register_blueprint(db)
    app.register_blueprint(register)
    app.register_blueprint(login)
    
    return app
