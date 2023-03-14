from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.admin import Admin
from flask_app.models.user import User
from flask_app.models.employee import Employee
from flask_app.models.adresse import Address
from flask_app.models.type import Type
from flask_app.models.booking import Booking

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)



# #login employee with validate form 
@app.route('/employees/login')
def login_employees():
    
    return render_template("login_employee.html")

@app.route('/employees/login', methods=['POST'])
def login_employee():
    employee = Employee.get_by_email(request.form)
    if not employee:
        flash('Invalid email or password',"login")
        return render_template("login_employee.html")
    if not bcrypt.check_password_hash(employee.password, request.form['password']):
        flash('Invalid email or password',"login")
        return render_template("login_employee.html")
    session['employee_id']=employee.id
    #logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    my_bookings = Booking.get_employee_bookings({"employee_id":session['employee_id']})
    for b in my_bookings:
        print(b.start_date, b.end_date)
    return render_template('book_employee.html', employee=employee ,my_bookings=my_bookings)
    



#login employee with validate form 
@app.route('/add/employee')
def create_employee():

    types=Type.get_all_types()
    
    return render_template("registration_employees.html", types=types)
    
    

#register employee with validate form 
@app.route('/create/employee', methods=['post'])
def add_employee():
    if not Employee.validate_employee(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(session['admin_id'])
    data = {
        **request.form,
        'password': pw_hash, 'admin_id':session['admin_id']
        
    }
    print(data,"*"*20)
    address_id = Address.create_address(request.form)
    print(address_id,"-"*25)
    data = {
        **data, "address_id": address_id
        
    }
    employee_id = Employee.create_employee(data)
    session['employee_id'] = employee_id
    employees = Employee.get_by_id({'id':employee_id})

    #return redirect(f'/employee/dashboard/{employee_id}')
    return redirect('/dashboard')
    


@app.route('/employee/<int:employee_id>')
def employee_profile(employee_id):
    # if 'employee_id' not in session:#if he has not an id redirect to the register page
    #     return redirect('/')
    employees = Employee.get_employees()
    #types=Type.get_by_id({'id':session['type_id']})

    return render_template("employee_profile.html", employees=employees)

#------edit employee 
@app.route('/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):

    employees = Employee.get_by_id({'id':employee_id})

    #logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    return render_template('edit_employee.html', employees=employees)


@app.route('/employee/update', methods=['POST'])
def update_employee():
    

    Employee.update_employee(request.form)
    data ={ 
        **request.form,
        'id':request.form['address_id']}
    print(f"------------{request.form}")
    Address.update_address (data)
    return redirect (f'/show/employee/{request.form["id"]}')


