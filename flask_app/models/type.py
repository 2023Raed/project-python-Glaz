from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user
from flask_app.models import employee

class Type():
    def __init__(self,data):
        self.id = data['id']
        self.type = data['type']

    @classmethod
    def create_type(cls,data):
        query="INSERT INTO employee_types (type)VALUES (%(type)s);"
        # this query will return the id of the new type insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all bookings
    @classmethod
    def get_all_types(cls):
        query="SELECT * FROM employee_types;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        types=[]
        for row in results:
            types.append(cls(row))
        print(types)
        return types
    
    #get one type by id
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM employee_types WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])

    #get one type by type
    @classmethod
    def get_by_type(cls,data):
        query="SELECT * FROM employee_types WHERE type=%(type)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])


    
    