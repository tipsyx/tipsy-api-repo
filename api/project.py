from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
import subprocess
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    job = db.Column(db.String(100))
    
    def __init__(self, name, age, gender, email, phone_number, job):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone_number = phone_number
        self.job = job

def create_database():
    with app.app_context():
        db.create_all()

# Helper function for handling database integrity errors
def handle_integrity_error(error=None):
    db.session.rollback()
    return jsonify({'Response Error Message': 'Database integrity error. Check your input data.'}), 400

# CREATE: Add a new person using curl
def create_person():
    new_person_data = [
        {
            "name": "John Doe",
            "age": 30,
            "gender": "Male",
            "email": "johndo@gmail.com",
            "phone_number": "08038127748",
            "job": "Software Engineer"
        },
        {
            "name": "Jane Doe",
            "age": 23,
            "gender": "Female",
            "email": "jdoe12@gmail.com",
            "phone_number": "08024987654",
            "job": "Data Analyst"
        },
        {
            "name": "Jane Smith",
            "age": 25,
            "gender": "Female",
            "email": "janesmith1995@yahoo.com",
            "phone_number": "07055565555",
            "job": "Marketing Manager"
        },
        {
            "name": "Smith Johnson",
            "age": 35,
            "gender": "Male",
            "email": "smithjohnson@example.com",
            "phone_number": "111-222-3333",
            "job": "Teacher"
        }
    ]
   
    curl_command = f'curl -X POST -H "Content-Type: application/json" -d \'{json.dumps(new_person_data)}\' http://localhost:8000/api'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    print(result.stdout)

# Function to retrieve all people using curl
def get_all_people():
    curl_command = 'curl https://api-to-perform-crud.onrender.com/api'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    print(result.stdout)

# Function to update a specific person using curl
def update_person(user_id):
    updated_person_data = {
        "name": "Samantha Johnson",
        "gender": "Female",
        "phone_number": "123-456-7890",
        "job": "Updated Job"
    }
    curl_command = f'curl -X PUT -H "Content-Type: application/json" -d \'{json.dumps(updated_person_data)}\' http://localhost:8000/api/{user_id}'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    print(result.stdout)

# Function to delete a specific person using curl
def delete_person(user_id):
    curl_command = f'curl -X DELETE http://localhost:8000/api/{user_id}'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    print(result.stdout)

# CREATE: Add a new person
@app.route('/api', methods=['POST'])
def add_person():
    data_list = request.get_json()
    
    if not isinstance(data_list, list):
        return jsonify({'Response Error Message': 'Invalid JSON data. Expected a list of persons.'}), 400
    
    for data in data_list:
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        email = data.get('email')
        phone_number = data.get('phone_number')
        job = data.get('job')
        
        if not name or not age:
            return jsonify({'Response Error Message': 'Name and age are required for each person'}), 400
        
        try:
            person = Person(
                name=name,
                age=age,
                gender=gender,
                email=email,
                phone_number=phone_number,
                job=job
            )
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'Response Error Message': 'Database integrity error. Check your input data.'}), 400
    
    return jsonify({'Successful Response Message': 'Persons added successfully'}), 201

# READ: Fetch details of a person by ID
@app.route('/api/<int:user_id>', methods=['GET'])
def get_person(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({'Fetch Error Message': 'Person not found'}), 404
    return jsonify({
        'Name': person.name,
        'Age': person.age,
        'Gender': person.gender,
        'Email': person.email,
        'Phone Number': person.phone_number,
        'Job': person.job
    })

# GET: Retrieve a list of all persons
@app.route('/api', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    person_list = [{
        'Name': person.name,
        'Age': person.age,
        'Gender': person.gender,
        'Email': person.email,
        'Phone Number': person.phone_number,
        'Job': person.job
    } for person in persons]
    return jsonify({'persons': person_list})

# UPDATE: Modify details of an existing person by ID
@app.route('/api/<int:user_id>', methods=['PUT'])
def update_person_route(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({'Fetch Error Message': 'Person not found'}), 404
    
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    email = data.get('email')
    phone_number = data.get('phone_number')
    job = data.get('job')
        
    if name is not None:
        person.name = name
    if age is not None:
        person.age = age
    if gender is not None:
        person.gender = gender
    if email is not None:
        person.email = email
    if phone_number is not None:
        person.phone_number = phone_number
    if job is not None:
        person.job = job
    
    try:
        db.session.commit()
        return jsonify({'Update message': 'Person updated successfully'})
    except IntegrityError:
        return handle_integrity_error()

# DELETE: Remove a person by ID
@app.route('/api/<int:user_id>', methods=['DELETE'])
def delete_person(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({'Fetch Error Message': 'Person not found'}), 404
    
    try:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'Delete message': 'Person deleted successfully'})
    except IntegrityError:
        return handle_integrity_error()

# Route for the root URL ("/")
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Home': '''
        Welcome to the Tipsy API. 
        This API is designed to perform CRUD (Create, Read, Update, Delete) operations on a database of people records. 
        It provides a simple interface to manage information about individuals, including their names, ages, etc.
    '''})

if __name__ == '__main__':
    create_database()
    port = int(os.environ.get('PORT', 8000))
    debug = bool(os.environ.get('DEBUG', False))
    app.run(host='0.0.0.0', port=port)

