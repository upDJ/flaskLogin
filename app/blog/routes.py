from flask import Blueprint, request
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
    #make sure user cannot make more than 2 posts per day
    # AND post_date > (NOW() - (1 * (60 * 60 * 24)))
    posts_in_last_24_hours =  cur.execute("""
                                SELECT*, (select count(*) FROM blogs WHERE user_id = {} AND post_date > (NOW() - (1 * (60 * 60 * 24))))
                                AS count FROM blogs WHERE user_id = {} ORDER BY user_id AND post_date > (NOW() - (1 * (60 * 60 * 24)));
                                """.format(user_id, user_id))
    mysql.connection.commit()
    print(posts_in_last_24_hours)
    if posts_in_last_24_hours < 2: #switch
        #post blog
        cur.execute("INSERT INTO blogs(subject, description, tags, user_id) VALUES ( %s, %s, %s, %s)", (subject, description, tags, user_id))
        mysql.connection.commit()
        cur.close()
        return "Data Stored \n subject: {} description: {}\n tags: {} user_id: {}".format(subject, description, tags, user_id), 200
    else:
        return "Post Limit Exceeded", 500