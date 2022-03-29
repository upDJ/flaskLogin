
from flask import Blueprint

from app import mysql

db = Blueprint('db', __name__, url_prefix='/db')
    
@db.route('/init', methods=['GET'])
def init_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE IF EXISTS user;")
        cur.execute("""
            CREATE TABLE `user` (
            `username` varchar(20) NOT NULL,
            `password` varchar(20) DEFAULT NULL,
            `firstName` varchar(20) DEFAULT NULL,
            `lastName` varchar(20) DEFAULT NULL,
            `email` varchar(20) DEFAULT NULL,
            PRIMARY KEY (`username`),
            UNIQUE KEY `email` (`email`)
            );"""
        )
        mysql.connection.commit()
        cur.close()
        return "initializing db", 200
    except ValueError:
        return "Error initializing db", 500

