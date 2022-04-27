from flask import Blueprint, request
from sqlalchemy import except_all
from app import mysql
import json

blog = Blueprint('blog', __name__, url_prefix='/blog')


@blog.route('/all', methods=['GET'])
def get_all_posts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT subject, description, tags FROM blogs")
        rows = cur.fetchall()
        mysql.connection.commit()
        blogs = json.dumps(rows, sort_keys=True, indent=4)
        print(blogs)
        return blogs, 200
    except ValueError:
        return "Error Getting Blog Posts", 500


@blog.route('/', methods=['POST'])
def create_blog_post():
    obj = request.json
    subject = obj['subject']
    description = obj['description']
    tags = json.dumps(obj["tags"])
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
    print(posts_in_last_24_hours)
    if posts_in_last_24_hours < 2:  # switch
        # post blog
        cur.execute("INSERT INTO blogs(subject, description, tags, user_id) VALUES ( %s, %s, %s, %s)",
                    (subject, description, tags, user_id))
        mysql.connection.commit()
        cur.close()
        return "Data Stored \n subject: {} description: {}\n tags: {} user_id: {}".format(subject, description, tags, user_id), 200
    else:
        return "Post Limit Exceeded", 500


@blog.route('/twoblogs', methods=['GET'])
def getUsersTwoBlogs():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT firstName, lastName, email, id
                    FROM `comp440`.`user` AS U
                    INNER JOIN(SELECT user_id, COUNT(*) AS cc
                            FROM `comp440`.`blogs`
                            GROUP BY user_id
                            HAVING COUNT(user_id) > 1) AS B
                    ON B.user_id=U.id
                    GROUP BY user_id
                    """)
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
        query = """SELECT DISTINCT B.id, subject, description, tags, C.rating FROM `comp440`.`blogs` AS B
                    INNER JOIN `comp440`.`comments` AS C
                    ON C.blog_id = B.id 
                    WHERE C.rating = 'positive'
                    AND B.user_id = ( SELECT id FROM `comp440`.`user` AS U WHERE id = {})
                """.format(user_id)

        cur.execute(query)
        rows = cur.fetchall()
        blogs = json.dumps(rows, sort_keys=True, indent=3)
        print(blogs)
        return blogs, 200
    except ValueError:
        return "Error Getting Up Voted Blogs", 500
