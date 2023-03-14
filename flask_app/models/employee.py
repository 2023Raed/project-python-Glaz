from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app import DATABASE
from flask_app.models import admin 
from flask_app.models import type 
from flask_app.models import adresse
from flask_app.models import booking

class Employee():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.cv = data['cv']
        self.video = data['video']
        self.phone_number = data['phone_number']
        self.cin = data['cin']
        self.price_per_hour = data['price_per_hour']
        self.admin_id = data['admin_id']
        self.type_id=data ['type_id']
        self.address_id = data['address_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.admin = admin.Admin.get_by_id({'id':self.admin_id})
        self.address = adresse.Address.get_by_id({'id':self.address_id})
        self.type = type.Type.get_by_id({'id':self.type_id})
        self.my_bookings = booking.Booking.get_employee_bookings({"employee_id":self.id})

    #**********CRUD Queries**********
    @classmethod
    def create_employee(cls,data):
        query="""
        INSERT INTO employees (first_name,last_name,email,address_id,type_id,
        password,cv,video,phone_number,cin,price_per_hour,admin_id)

        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(address_id)s,
        %(type_id)s,%(password)s,%(cv)s,%(video)s,%(phone_number)s,
        %(cin)s,%(price_per_hour)s,%(admin_id)s);
        """
        # this query will return the id of the new employee insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all employee
    @classmethod
    def get_employees(cls):
        query="SELECT * FROM employees;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        employees=[]
        for row in results:
            employees.append(cls(row))
        return employees
    
    #get one employee by id
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM employees WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    

    #get one employee by email
    @classmethod
    def get_by_email(cls,data):
        query="SELECT * FROM employees WHERE email=%(email)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])
    @classmethod
    def update_employee(cls, data):
        query = """
        UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, 
        password = %(password)s, cv = %(cv)s, video= %(video)s,
        phone_number = %(phone_number)s, cin = %(cin)s, price_per_hour = %(price_per_hour)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)    
    
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM employees WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def show_employees(cls,data):
        query="""
        select * from employees JOIN employee_types ON employees.type_id= employee_types.id WHERE employees.type_id=%(type_id)s;
        """
        result= connectToMySQL(DATABASE).query_db(query,data)

        all_employees = []
        for row in result:
            all_employees.append(cls(row))
        return all_employees

    #validate employee
    @staticmethod
    def validate_employee(data):
        is_valid = True
        if len(data['first_name'])<2:
            flash("First Name must be more than 2 characters!","register")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Last Name must be more than 2 characters!","register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email must be valid !","register")
            is_valid = False
        elif Employee.get_by_email({'email':data['email']}):
            flash("Email already exist !","register")
            is_valid = False
        if len(data['password'])<6:
            flash("Password must be more than 6 characters!","register")
            is_valid = False
        elif data['password']!=data['confirm_password']:
            flash("Passwords do not match!","register")
            is_valid = False

        return is_valid

