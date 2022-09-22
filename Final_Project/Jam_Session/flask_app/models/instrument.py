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
        query = "UPDATE instruments SET instrument=%(instrument)s, years=%(years)s, WHERE id= %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_instrument(cls, data):
        query = 'SELECT * FROM instruments JOIN users ON instruments.user_id = users.id WHERE users.id = %(id)s'
        results = connectToMySQL(db).query_db(query, data)
        instruments = []
        for row in results:
            user = cls(row)
            user_data = {
                'id' : row['users.id'],
                'username' : row['username'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'state' : row['state'],
                'password' : row['password'],
                'zip_code' : row['zip_code'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            user.instrument = User(user_data)
            instruments.append(instruments)
        return instruments

    @classmethod
    def save(cls, data):
        query="INSERT INTO intruments (instrument, years, user_id) VALUES (%(instrument)s, %(user_id)s)"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_all_instruments(cls):
        query  = "SELECT * FROM instruments LEFT JOIN users ON instruments.user_id = users.id"
        result = connectToMySQL(db).query_db(query)
        instruments = []
        
        for instrument in result:
            instruments.append(cls(instrument))
        return instruments

    @classmethod
    def remove():
        query = 'DELETE FROM instruments where id = %(id)s'
        return connectToMySQL(db).query_db(query)