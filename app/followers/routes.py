from flask import Blueprint, request
from app import mysql
import json

followers = Blueprint('followers', __name__, url_prefix='/followers')

@followers.route('/insert', methods=['POST'])
def postUserFollowers():
    try:
        obj = request.json
        username = obj['username'] #of person to follow
        user_id = obj['user_id']
        print(type(username), type(user_id))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO followers(username, user_id) VALUES(%s, %s)", (username, user_id))
        mysql.connection.commit()
        cur.close()
        return "success", 200
    except ValueError:
        return "Error Posting Hobbies", 500
        