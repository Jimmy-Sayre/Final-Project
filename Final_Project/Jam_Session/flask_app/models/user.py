from flask_app.config.mysqlconnection import connectToMySQL
import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

db = 'jam_session'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.state = data['state']
        self.zip_code = data['zip_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def login(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def register(cls,data):
        query = "INSERT INTO users (username,first_name,last_name,email,password) VALUES(%(username)s,%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def validate_register(cls, data):
        is_valid = True
        if len(data['first_name']) == 0 or len(data['last_name']) == 0 or len(data['email']) == 0 or len(data['password']) == 0:
            flash("All fields required")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid","register")
            is_valid=False
        if len(data['username']) < 3:
            flash("Username must be at least 3 characters","register")
            is_valid=False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
        return is_valid

    @classmethod
    def get_one(cls,data):
        query = " SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET username=%(username)s, first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, state=%(state)s, zip_code=%(zip_code)s WHERE id= %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query  = "SELECT * FROM users LEFT JOIN instruments ON user_id = users.id"
        result = connectToMySQL(db).query_db(query)
        users = []
        
        for user in result:
            users.append(cls(user))
        return users

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)