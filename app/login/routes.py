from flask import Blueprint, jsonify, request
from app import mysql

login = Blueprint('login', __name__, url_prefix='/login')


@login.route('/', methods=['POST'])
def login_user():
    # Check if "username" and "password" POST requests exist
   
    json = request.json
    email = json['email']
    name = json['name']
    password = json['password']
    print(json)
    # check if user is in the database
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM user WHERE email = %s AND username = %s AND password = %s', (email, name, password))
    user = cur.fetchone()

    if user:
        print(user)
        return {"state": "Logged In", "username": user }, 200
        
    return 'Invalid Info', 404
    
