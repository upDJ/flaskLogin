from flask import Blueprint, request
from app import mysql
import json

hobby = Blueprint('hobby', __name__, url_prefix='/hobby')

@hobby.route('/insert', methods=['POST'])
def postUserHobbies():
    try:
        obj = request.json
        user_id = obj['user_id']
        hobbies = obj['hobby']
        print(hobbies)
        cur = mysql.connection.cursor()
        for hobby in hobbies:
            print(hobby)
            cur.execute("INSERT INTO hobby(hobby, user_id) VALUES(%s, %s)", (hobby, user_id))
            mysql.connection.commit()
        cur.close()
        return {'hobby': hobby, 'user_id': user_id}, 200
    except ValueError:
        return "Error Posting Hobbies", 500

@hobby.route('/common', methods=['GET'])
def find_common_hobby_pair():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT a.user_id, b.user_id,
                        GROUP_CONCAT(DISTINCT a.hobby) AS 'Common hobbies'
                        FROM hobby a
                        JOIN hobby b ON a.user_id < b.user_id
                        AND a.hobby LIKE b.hobby
                        GROUP BY a.user_id, b.user_id
                        LIMIT 1
                    """)
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows)
        cur.close()
        print(users)
        return users, 200
    except ValueError:
        return "Error Getting Users", 500


        