from flask import Blueprint, request
from app import mysql

login = Blueprint('login', __name__, url_prefix='/login')

@login.route('/',methods=['GET','POST'])
def login_user():
      # Check if "username" and "password" POST requests exist 
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        #check if user is in the database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM accounts WHERE email = %s AND username = %s AND password = %s', (email, name, password))
        user = cur.fetchone()
        
        if user:
            return 'Logged In', 200
        else:
            return 'Invalid Info', 404

    