#!/#path/#to##python

#Returning json data for client
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initilize app

app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initial Database
db = SQLAlchemy(app)

#Initial Marshmallow
ma = Marshmallow(app)

#Employee Class
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    job = db.Column(db.String(200))
    school = db.Column(db.String(100))
    age = db.Column(db.Integer)
    
    def __init__(self, name, job, school, age):
        self.name = name
        self.job = job
        self.school = school
        self.age = age
        

#Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('name', 'job', 'school', 'age')

# Initialize Schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many = True)

# Create an Employee
@app.route('/employee', methods = ['POST'])
def add_Employee():
    name = request.json['name']
    job = request.json['job']
    id = request.json['id']
    school = request.json['school']
    age = request.json['age']
    
    new_employee = Employee(name, job, id, school, age)
    db.session.add(new_employee)
    db.session.commit()
    return employee_schema.jsonify(new_employee)

#Get All Employees
@app.route('/employee', methods = ['GET'])
def get_employees():
    all_employees= Employee.query.all()
    result = employees_schema.dump(all_employees) #Multiple employees
    return jsonify(result.data)
    
    
# Get Single Employee
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

# Update an Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    name = request.json['name']
    job = request.json['job']
    id = request.json['id']
    school = request.json['school']
    age = request.json['age']]

    employee.name = name
    employee.job = job
    employee.id = id
    employee.school = school
    employee.age = age

    db.session.commit()

    return employee_schema.jsonify(employee)

# Delete Employee
@app.route('/product/<id>', methods=['DELETE'])
def delete_employee(name):
    employee = Employee.query.get(name)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


#Run server
if __name__ == "__main__":
    app.run(debug=True)
