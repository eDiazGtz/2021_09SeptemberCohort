from books_app import app
from books_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    db = "fav_books"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def register_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE users.id = %(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_one_by_email(cls, data):
        query = 'SELECT * FROM users WHERE users.email = %(email)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        user = cls(results[0])
        return user
    
    @staticmethod
    def valid_registration(data):
        #true or false
        is_valid = True
        # Email Format Validation
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        # Unique Email Validation
        user = User.get_one_by_email(data)
        if user:
            flash('Email already in use')
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First Name must be at least 2 characters')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last Name must be at least 2 characters')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_valid = False
        if data['password'] != data['password_confirm']:
            flash('Passwords must match')
            is_valid = False
        return is_valid

    @staticmethod
    def valid_login(data):
        is_valid = True
        user = User.get_one_by_email(data)
        if not user:
            is_valid = False
            flash('Invalid Input')
        if not bcrypt.check_password_hash(user.password, data['password']):
            is_valid = False
            flash('Invalid Input')
        return is_valid