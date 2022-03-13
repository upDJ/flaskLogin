from flask import Blueprint

register = Blueprint('register', __name__, url_prefix='/register')

@register.route('/')
def create_user():
    return "register user"


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         details = request.form
#         #should be model
#         username = details['user']
#         password = details['pass']
#         firstName = details['fname']
#         lastName = details['lname']
#         email = details['email']
        
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO user(username, password, firstName, lastName, email) VALUES (%s, %s, %s, %s, %s)", (username, password, firstName, lastName, email))
#         mysql.connection.commit()
#         cur.close()
#         return "Data Stored \n user: {} pass: {}\n firstname: {} lastname: {}\n email: {}".format(username, password, firstName, lastName, email)