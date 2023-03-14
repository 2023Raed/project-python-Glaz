from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user
from flask_app.models import employee

class Booking():
    def __init__(self,data):
        self.booking_id = data['id']
        self.is_confirmed = data['is_confirmed']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.start_hour = data['start_hour']
        self.end_hour = data['end_hour']
        self.employee_id = data['employee_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = user.User.get_by_id({'id':self.user_id})

        self.employee =None

    @classmethod
    def create_booking(cls,data):
        query="INSERT INTO bookings (is_confirmed,start_date,end_date,start_hour,end_hour,employee_id,user_id)VALUES (1,%(start_date)s,%(end_date)s,%(start_hour)s,%(end_hour)s,%(employee_id)s,%(user_id)s);"
        # this query will return the id of the new booking insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all bookings
    @classmethod
    def get_bookings(cls):
        query="SELECT * FROM bookings;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        bookings=[]
        for row in results:
            bookings.append(cls(row))
        return bookings


    @classmethod
    def get_employee_bookings(cls, data):
        query="SELECT * FROM bookings WHERE employee_id = %(employee_id)s;"
        results= connectToMySQL(DATABASE).query_db(query,data)
        #organize the results
        print("*"*20,results,"*"*20)
        bookings=[]
        for row in results:
            bookings.append(cls(row))
        print("-"*20,results,"-"*20)
        return bookings
    #get one booking by id
    @classmethod
    def get_booking_by_id(cls,data):
        query="SELECT * FROM bookings WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    
    # update one booking
    @classmethod
    def update(cls, data):
        query = """UPDATE bookings SET is_confirmed=%(is confirmed)s,start_date=%(start_date)s,end_date=%(end_date)s
        ,start_hour=%(start_hour)s,end_hour=%(end_hour)s,employee_id=%(employee_id)s,user_id=%(user_id)s
        WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
        
    #  delete booking
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM bookings WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
