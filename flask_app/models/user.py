from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app import DATABASE
from flask_app.models.adresse import Address


class User():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address_id = data['address_id']
        self.password = data['password']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address = Address.get_by_id({'id':self.address_id})


    #**********CRUD Queries**********
    @classmethod
    def create_user(cls,data):
        query="""
        INSERT INTO users (first_name,last_name,email,address_id,password,phone_number) 
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(address_id)s,%(password)s,%(phone_number)s);
        """
        # this query will return the id of the new user insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all users
    @classmethod
    def get_users(cls):
        query="SELECT * FROM users;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        users=[]
        for row in results:
            users.append(cls(row))
        return users
    
    #get one user by id
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    

    #get one user by email
    @classmethod
    def get_by_email(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])
    @classmethod
    def update_user(cls, data):
        query = """UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,address_id=%(address_id)s
        ,password=%(password)s,phone_number=%(phone_number)s
        WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)    
    
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM users WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)

    #validate user
    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name'])<2:
            flash("First Name must be more than 2 characters!","register")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Last Name must be more than 2 characters!","register")
            is_valid = False
        # if len(data['address_id'])<2:
        #     flash("Address must be more than 2 characters!","register")
        #     is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email must be valid !","register")
            is_valid = False
        elif User.get_by_email({'email':data['email']}):
            flash("Email already exist !","register")
            is_valid = False
        if len(data['password'])<6:
            flash("Password must be more than 6 characters!","register")
            is_valid = False
        elif data['password']!=data['confirm_password']:
            flash("Passwords do not match!","register")
            is_valid = False

        return is_valid