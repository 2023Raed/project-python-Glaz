from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.user import User

from flask_app.models.employee import Employee
from flask_app.models.adresse import Address
from flask_app.models.booking import Booking

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/users/services')
def services():
    return render_template("dashboard.html") 
@app.route('/users/about_us')
def about_us():
    return render_template("about_us.html") 

@app.route('/users/contact_us')
def contact_us():
    return render_template("contactUs.html")

#register user with validate form 
@app.route('/users/register')
def register():
    
    return render_template("registration_user.html")

#register user with validate form 
@app.route('/users/create', methods=['post'])
def Add_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': pw_hash
    }
    address_id = Address.create_address (request.form)
    data = {
        **request.form, "address_id": address_id

        
    }
    user_id = User.create_user(data)
    session['user_id'] = user_id
    return redirect('/users/dashboard')

@app.route('/users/login')
def user_login():
    return render_template("login.html")


#Login user with validate form
@app.route('/users/login',methods=['POST'])
def login():
    user_db = User.get_by_email(request.form)
    if not user_db:
        flash('Invalid email or password',"login")
    #     return redirect('/')
    # if not bcrypt.check_password_hash(user_db.password, request.form['password']):
    #     flash('Invalid email or password',"login")
    #     return redirect('/')
    session['user_id']=user_db.id
    return redirect('/users/dashboard')

@app.route('/users/dashboard')
def dashboard():

    if 'user_id' not in session:#if he has not an id redirect to the register page
        return redirect('/')
    log_user=User.get_by_id({'id':session['user_id']})
    all_employees = Employee.get_employees()

    return render_template("dashboard.html",log_user=log_user, all_employees= all_employees)

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):

    users = User.get_by_id({'id':user_id})

    #logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    return render_template('edit_user.html', users=users)

# @app.route('/users/show')
# def show_user():
#     log_user=User.get_by_id({'id':session['user_id']})
#     return render_template("user_profile.html", log_user=log_user)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#user show employee 
@app.route('/show/employee/<int:employee_id>')
def get_employee(employee_id):

    employees = Employee.get_employees({'id':employee_id})
    logged_user=User.get_by_id({'id':session['user_id' ]})
    return render_template('employees.html', employees=employees, logged_user=logged_user)

@app.route('/users/shows')
def show_users():
    log_user=User.get_users()
    return render_template("customers.html", log_user=log_user)

@app.route('/user/update', methods=['POST'])
def update_user():
    print(f"------------{request.form}")
    data ={ 
        **request.form,
        'id':request.form['address_id']}
    print(f"------------{request.form}")
    Address.update_address (data)
    User.update_user(request.form)
    return redirect ('/users/shows')    

@app.route('/book/<int:employee_id>')
def book(employee_id):
    employees = Employee.get_by_id({'id':employee_id})
    return render_template("booking.html",employee_id=employee_id)

@app.route('/book/employee/<int:employee_id>', methods=['POST'])
def make_booking(employee_id):
    data = {
        **request.form,
        'employee_id': employee_id,
        'user_id': session['user_id']
        
    }
    Booking.create_booking(data)
    return redirect (f'/book/message/{data["user_id"]}')

@app.route('/book/message/<int:user_id>')
def booking_message(user_id):
    user=User.get_by_id({'id':user_id})
    return render_template("message_booking.html", user=user)

    





