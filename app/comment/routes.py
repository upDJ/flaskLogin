from flask import Blueprint, request
from app import mysql

comment = Blueprint('comment', __name__, url_prefix='/comment')


@comment.route('/', methods=['POST'])
def create_comment():
    obj = request.json
    rating = obj['rating']
    comment = obj['comment']
    user_id = obj['user_id']
    blog_id = obj['blog_id']

    print(obj)
    cur = mysql.connection.cursor()
    # check to make sure the user isnt trying to comment on his own blog
    query1 = """SELECT * 
                FROM `comp440`.`blogs`
                WHERE id = {} AND user_id = {};""".format(blog_id, user_id)
    rows = cur.execute(query1)
    mysql.connection.commit()
    print(rows)
    if (rows == 0):
        # make sure user cannot make more than 3 comments per day
        # AND post_date > (NOW() - (1 * (60 * 60 * 24)))
        comments_in_last_24_hours = cur.execute("""
                                    SELECT*, (select count(*) FROM comments WHERE user_id = {} AND post_date > (NOW() - (1 * (60 * 60 * 24))))
                                    AS count FROM comments WHERE user_id = {} ORDER BY user_id AND post_date > (NOW() - (1 * (60 * 60 * 24)));
                                    """.format(user_id, user_id))
        mysql.connection.commit()
        print(comments_in_last_24_hours)
        if comments_in_last_24_hours < 3:
            # post comment
            cur.execute("INSERT INTO comments(rating, comment, user_id, blog_id) VALUES ( %s, %s, %s, %s)",
                        (rating, comment, user_id, blog_id))
            mysql.connection.commit()
            cur.close()
            return "Data Stored \n rating: {} comment: {}\n user_id: {}\n blog_id: {}".format(rating, comment, user_id, blog_id), 200
        else:
            return "Comment Limit Exceeded", 500
    else:
        return "user cannot comment on his own blog", 503
