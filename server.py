from flask_app import app

#import controllers here
from flask_app.controllers import employees
from flask_app.controllers import admins
from flask_app.controllers import users




if __name__ == '__main__':

    app.run(debug=True,port=5005 )