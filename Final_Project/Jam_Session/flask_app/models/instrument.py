from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User

db = 'jam_session'

class Instrument:
    def __init__( self , data ):
        self.id = data['id']
        self.instrument = data['instrument']
        self.years = data['years']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def add_instrument(cls,data):
        query = "INSERT INTO instruments (instrument, years, user_id) VALUES(%(instrument)s,%(years)s, %(user_id)s)"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE instruments SET intrument=%(instrument)s, years=%(years)s, WHERE id= %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_instrument(cls, data):
        query = 'SELECT * FROM instruments JOIN users ON instrument.user_id = users.id WHERE users.id = %(id)s'
        results = connectToMySQL(db).query_db(query, data)
        instruments = cls(results[0])
        for row in results:
            user_data = {
                'id' : row['users.id'],
                'username' : row['username'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            instruments.user = User(user_data)
        return instruments