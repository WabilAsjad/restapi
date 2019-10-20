#!/#path/#to##python

#Returning json data for client
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initialize app

app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initial Database
database = SQLAlchemy(app)

#Initial Marshmallow
ma = Marshmallow(app)

#Employee Class
class Employee(database.Model): 
    name = database.Column(database.String(100), unique = True)
    job = database.Column(database.String(200))
    identity = database.Column(database.Integer, primary_key = True)
    school = database.Column(database.String(100))
    age = database.Column(database.Integer)
    
    def __init__(self, name, job, identity, school, age):
        self.name = name
        self.job = job
        self.identity = identity
        self.school = school
        self.age = age
        
#Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('name', 'job', 'identity', 'school', 'age')

# Initialize Schema for database
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many = True)

# Create an Employee 
@app.route('/employee', methods = ['POST'])
def add_Employee():
    name = request.json['name']
    job = request.json['job']
    identity = request.json['identity']
    school = request.json['school']
    age = request.json['age']
    
    #Add employee to database and return in json format
    new_employee = Employee(name, job, identity, school, age)
    database.session.add(new_employee)
    database.session.commit()
    return employee_schema.jsonify(new_employee)

#Get All Employees
@app.route('/employee', methods = ['GET'])
def get_employees():
    all_employees= Employee.query.all()
    result = employees_schema.dump(all_employees) #Multiple employees
    return jsonify(result.data)
    
#Get Single Employee
@app.route('/employee/<identity>', methods=['GET'])
def get_employee(identity):
    employee = Employee.query.get(identity)
    return employee_schema.jsonify(employee)

#Update an Employee in database
@app.route('/employee/<identity>', methods=['PUT'])
def update_employee(identity):
    employee = Employee.query.get(identity)

    name = request.json['name']
    job = request.json['job']
    identity = request.json['identity']
    school = request.json['school']
    age = request.json['age']

    employee.name = name
    employee.job = job
    employee.id = identity
    employee.school = school
    employee.age = age

    database.session.commit()

    return employee_schema.jsonify(employee)

#Delete Employee from database
@app.route('/employee/<name>', methods=['DELETE'])
def delete_employee(name):
    employee = Employee.query.get(name)
    database.session.delete(employee)
    database.session.commit()

    return employee_schema.jsonify(employee)

#Run server
if __name__ == "__main__":
    app.run(debug=True)
