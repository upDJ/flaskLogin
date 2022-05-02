from flask import Blueprint, request
from app import mysql
import json

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/all')
def get_all():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, firstName, lastName, username FROM user")
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows, sort_keys=True, indent=4)
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500

@user.route('/ondate', methods=['GET'])
def on_date():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
                    SELECT username, B.max_users FROM user
                    INNER JOIN (
                    SELECT user_id, MAX(user_id) AS max_users
                    FROM blogs
                    WHERE post_date BETWEEN '2022-05-02 00:00:00' AND '2022-05-02 23:59:59'
                    GROUP BY user_id) AS B
                    WHERE id = user_id
                    """)
        rows = cur.fetchall()
        mysql.connection.commit()
        data = json.dumps(rows)
        users = json.loads(data)
        
        max_count = 0
        
        #find max
        for user in users:
            if user[1] > max_count:
                max_count = user[1]
        
        #store users with max count
        result_users = []
        for user in users:
            if user[1] == max_count:
                result_users.append(user)   
        result = json.dumps(result_users)
        print(result)
        return result , 200
    except ValueError:
        return "Error Getting Users", 500

@user.route('/followedBy')
def followed_by_both():
    try:
        obj = request.args
        user1 = obj['first']
        user2 = obj['second']

        print(user1,user2)
        cur = mysql.connection.cursor()
        cur.execute("""SELECT username
                        FROM USER
                        WHERE username IN (SELECT username FROM followers WHERE user_id = '{}') 
                        AND username IN (SELECT username FROM followers WHERE user_id = '{}')
                    """.format(user1, user2))
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows)
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500
    
@user.route('/noblog')
def get_users_noblog():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT firstName, lastName
                        FROM user
                        WHERE id NOT IN (SELECT user_id FROM blogs)
                    """)
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows)
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500
    
@user.route('/nocomment')
def get_users_nocomment():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT firstName, lastName
                        FROM user
                        WHERE id NOT IN (SELECT user_id FROM comments)
                    """)
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows)
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500

@user.route('/negative')
def get_negative_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT firstName, lastName FROM user 
                        WHERE id IN (
                        SELECT user_id
                                    FROM comments
                                    WHERE rating = "negative"
                        )
                        AND id NOT IN (
                        SELECT user_id
                                    FROM comments
                                    WHERE rating = "positive"
                    )""")
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows)
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500
    
@user.route('/allpositive')
def get_positive_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT firstName, lastName
                        FROM user
                        WHERE id in(
                                SELECT user_id
                                FROM blogs
                                WHERE id NOT IN (
                                    SELECT blog_id
                                    FROM comments
                                    WHERE rating = "negative"
                                    GROUP BY blog_id
                                    HAVING COUNT(rating) > 0)
                    )""")
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows)
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500

    