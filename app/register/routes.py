from flask import Blueprint, request
from app import mysql

register = Blueprint('register', __name__, url_prefix='/register')

@register.route('/')
def create_user():
    return "register user"


@register.route('/', methods=['POST'])
def index():
    json = request.json
    username = json['uname']
    password = json['pass']
    firstName = json['fname']
    lastName = json['lname']
    email = json['email']
    cur = mysql.connection.cursor()
    
    #check for duplicate
    cur.execute(
        'SELECT * FROM user WHERE email = %s AND username = %s AND password = %s', (email, username, password))
    user = cur.fetchone()
    if user:
        return "User already in database", 400

    cur.execute("INSERT INTO user(username, password, firstName, lastName, email) VALUES (%s, %s, %s, %s, %s)", (username, password, firstName, lastName, email))
    mysql.connection.commit()
    cur.close()
    return "Data Stored \n user: {} pass: {}\n firstname: {} lastname: {}\n email: {}".format(username, password, firstName, lastName, email), 200