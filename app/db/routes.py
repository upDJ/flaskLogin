
from flask import Blueprint

from app import mysql

db = Blueprint('db', __name__, url_prefix='/db')


@db.route('/init', methods=['GET'])
def init_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE IF EXISTS comp440.comments;")
        cur.execute("DROP TABLE IF EXISTS comp440.blogs;")
        cur.execute("DROP TABLE IF EXISTS comp440.user;")
        cur.execute("DROP TABLE IF EXISTS comp440.tag")
        mysql.connection.commit()
        cur.execute("""
            CREATE TABLE `user` (
            `id` INTEGER NOT NULL AUTO_INCREMENT,
            `username` varchar(20) NOT NULL,
            `password` varchar(20) NOT NULL,
            `firstName` varchar(20) NOT NULL,
            `lastName` varchar(20) NOT NULL,
            `email` varchar(30) NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY (`username`),
            UNIQUE KEY `email` (`email`)
            );""")
        mysql.connection.commit()
        cur.execute("""
            CREATE TABLE `blogs` (
            `id` INTEGER NOT NULL AUTO_INCREMENT,
            `subject` varchar(45) NOT NULL,
            `description` varchar(200) NOT NULL,
            `tags` JSON NOT NULL,
            `post_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
            `user_id` INTEGER NOT NULL,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
            );""")
        mysql.connection.commit()
        cur.execute("""
            CREATE TABLE `comments` (
            `id` INTEGER NOT NULL AUTO_INCREMENT,
            `rating` varchar(45) NOT NULL,
            `comment` varchar(100) NOT NULL,
            `post_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
            `user_id` INTEGER NOT NULL,
            `blog_id` INTEGER NOT NULL,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
            FOREIGN KEY (`blog_id`) REFERENCES `blogs` (`id`)
            );""")
        cur.execute("""
            CREATE TABLE `tag` (
            `id` INTEGER NOT NULL AUTO_INCREMENT,
            `topic` varchar(45) NOT NULL,
            `blog_id` INTEGER NOT NULL,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`blog_id`) REFERENCES `blogs` (`id`)
            );""")
        mysql.connection.commit()
        cur.close()
    except ValueError:
        return "Error initializing db", 500
    return "initializing db", 200
