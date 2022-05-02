from flask import Blueprint, request
from flask import Response
from sqlalchemy import except_all
from app import mysql
import json

blog = Blueprint('blog', __name__, url_prefix='/blog')

@blog.route('/all', methods=['GET'])
def get_all_posts():
    try:
        cur = mysql.connection.cursor()
        query = """SELECT id, subject, description, user_id FROM blogs"""
        cur.execute(query)
        rows = cur.fetchall()
        mysql.connection.commit()
        data = json.dumps(rows)
        data_arr = json.loads(data)
        
        # get tags associated to each blog
        blogs = {}
        for data in data_arr:
            id = str(data[0])
            print(id)
            query = """SELECT topic FROM tag WHERE blog_id='{}' """.format(id)
            cur.execute(query)
            rows = cur.fetchall()
            mysql.connection.commit()
            tags = json.dumps(rows)
            tags_arr = json.loads(tags)
            print(tags_arr)
            #format data
            blogs["blog"+id] = {"subject":data[1], "description":data[2], "tags": tags_arr}
        print(blogs)
        return blogs, 200
    except ValueError:
        return "Error Getting Blog Posts", 500


@blog.route('/', methods=['POST'])
def create_blog_post():
    obj = request.json
    subject = obj['subject']
    description = obj['description']
    tags = obj["tags"]
    print(tags)
    user_id = obj['user_id']
    print(obj)
    cur = mysql.connection.cursor()
    # make sure user cannot make more than 2 posts per day
    # AND post_date > (NOW() - (1 * (60 * 60 * 24)))
    posts_in_last_24_hours = cur.execute("""
                                SELECT*, (select count(*) FROM blogs WHERE user_id = {} AND post_date > (NOW() - (1 * (60 * 60 * 24))))
                                AS count FROM blogs WHERE user_id = {} ORDER BY user_id AND post_date > (NOW() - (1 * (60 * 60 * 24)));
                                """.format(user_id, user_id))
    mysql.connection.commit()

    if posts_in_last_24_hours < 2: 
        # post blog
        cur.execute("INSERT INTO blogs(subject, description, user_id) VALUES(%s, %s, %s)",
                    (subject, description, user_id))
        mysql.connection.commit()
        # post tags
        blog_id = cur.lastrowid
        for tag in tags:
            cur.execute(
                "INSERT INTO tag(topic, blog_id, user_id) VALUES(%s, %s, %s)", (tag, blog_id, user_id))
        mysql.connection.commit()
        cur.close()
        return "Data Stored \n subject: {} description: {}\n tags: {} user_id: {}".format(subject, description, tags, user_id), 200
    else:
        return Response("{'Error': 'User has excedded the amount of posts per day'}", status=500)


@blog.route('/filter', methods=['GET'])
def getUsersTwoBlogs():
    obj = request.args
    filter1 = obj.get('filter1')
    filter2 = obj.get('filter2')

    query = """SELECT username
                FROM user
                WHERE id IN (SELECT user_id FROM tag WHERE topic LIKE '{}'
                AND blog_id NOT IN (SELECT blog_id FROM tag WHERE topic LIKE '{}'))
                AND id IN (SELECT user_id FROM tag WHERE topic LIKE '{}'
                AND blog_id NOT IN (SELECT blog_id FROM tag WHERE topic LIKE '{}'))
                AND id IN (SELECT user_id FROM blogs 
                WHERE 2 <= (SELECT count(*) FROM blogs))
            """.format(filter1, filter2, filter2, filter1)
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        mysql.connection.commit()
        users = json.dumps(rows, sort_keys=True, indent=3)
        print('\nusers\' first name and last name fetched: ' + users)
        return users, 200
    except ValueError:
        return "Error Getting Users With Two Blogs", 500


@blog.route('/upvote/<user_id>', methods=['GET'])
def getUpVotedBlogs(user_id):
    try:
        print(user_id)
        cur = mysql.connection.cursor()
        query = """ SELECT id, subject, description, user_id FROM blogs 
                    WHERE id IN (
                    SELECT blog_id
                                FROM comments
                                WHERE rating = "positive"
                    )
                    AND id NOT IN(
                        SELECT blog_id
                                    FROM comments
                                    WHERE rating = "negative")
                    AND user_id="{}"
                """.format(user_id)

        cur.execute(query)
        rows = cur.fetchall()
        blogs = json.dumps(rows)
        print(blogs)
        return blogs, 200
    except ValueError:
        return "Error Getting Up Voted Blogs", 500
