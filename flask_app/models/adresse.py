from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Address():
    def __init__(self,data):
        self.id = data['id']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip_code = data['zip_code']

    @classmethod
    def create_address(cls,data):
        query="INSERT INTO addresses (street,city,state,zip_code) VALUES(%(street)s,%(city)s,%(state)s,%(zip_code)s);"
        # this query will return the id of the new address insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all addresses
    @classmethod
    def get_addresses(cls):
        query="SELECT * FROM addresses;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        addresses=[]
        for row in results:
            addresses.append(cls(row))
        return addresses
    
    #get one address by id
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM addresses WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def update_address(cls, data):
        query = """UPDATE addresses SET street=%(street)s,city=%(city)s,state=%(state)s,zip_code=%(zip_code)s
        WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data) 