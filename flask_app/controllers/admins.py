from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.admin import Admin
from flask_app.models.user import User
from flask_app.models.employee import Employee


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



#login admin with validate form 
@app.route('/admins/login')
def login_admin():
    
    return render_template("login_admin.html")


@app.route('/dashboard')
def dashboard_admin():
    if 'admin_id' not in session:
        return redirect('/')
    logged_admin = Admin.get_by_id({'id':session['admin_id']})
    all_employees = Employee.get_employees()
    all_users = User.get_users()
    return render_template("admin_dashboard.html", logged_admin = logged_admin , all_employees=all_employees, all_users=all_users)

@app.route('/admin/dashboard', methods=['post'])
def admin_admin():
    admin_from_db = Admin.get_by_email(request.form)
    if not admin_from_db:
        flash("Invalid Email / Password","login")
        return redirect('/')    
    # if not bcrypt.check_password_hash(admin_from_db.password, request.form['password']):
    #     flash("Invalid Email / Password","login")
        # return redirect('/')
    session['admin_id'] = admin_from_db.id
    return redirect ('/dashboard')

#login show employee 
@app.route('/show/employee/<int:employee_id>')
def show_employee(employee_id):

    employees = Employee.get_by_id({'id':employee_id})
    #logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    return render_template('employee_profile.html', employees=employees,employee_id=employee_id)

#login show employee 
@app.route('/services/employees/<int:type_id>')

def all_employees(type_id):

    employees = Employee.show_employees({'type_id':type_id})
    # logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    return render_template('employees.html', employees=employees, type_id=type_id)


@app.route('/employees/<int:employee_id>/delete')
def delete_employee(employee_id):

    employees = Employee.delete({'id':employee_id})
    #logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    return redirect('/dashboard')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):

    user = User.delete({'id':user_id})
    #logged_admin=Admin.get_by_id({'id':session['admin_id' ]})
    return redirect('/dashboard')
@app.route('/users/show/<int:user_id>')
def show_user(user_id):
    log_user=User.get_by_id({'id':session['user_id']})
    return render_template("user_profile.html", log_user=log_user)

