from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))#!/usr/bin/env python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

def create_database():
    with app.app_context():
        db.create_all()

# Helper function for handling database integrity errors
def handle_integrity_error(error=None):
    db.session.rollback()
    return jsonify({'Response Error Message': 'Database integrity error. Check your input data.'}), 400

# CREATE: Add a new person
@app.route('/api', methods=['POST'])
def add_person():
    data_list = request.get_json()

    if not isinstance(data_list, list):
        return jsonify({'Response Error Message': 'Invalid JSON data. Expected a list of persons.'}), 400

    for data in data_list:
        name = data.get('name')
        age = data.get('age')

        if not name or not age:
            return jsonify({'Response Error Message': 'Name and age are required for each person'}), 400

        try:
            person = Person(
                name=name,
                age=age,
            )
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'Response Error Message': 'Database integrity error. Check your input data.'}), 400

    return jsonify({'Successful Response Message': 'Persons added successfully'}), 201

# GET: Retrieve a list of all persons
@app.route('/api', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    person_list = [{
        'id': person.id,
        'name': person.name,
        'age': person.age,
    } for person in persons]
    return jsonify({'persons': person_list})

# READ: Fetch details of a person by ID
@app.route('/api/<int:user_id>', methods=['GET'])
def get_person(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({'Fetch Error Message': 'Person not found'}), 404
    return jsonify({
        'id': person.id,
        'name': person.name,
        'age': person.age,
    })

# UPDATE: Modify details of an existing person by ID
@app.route('/api/<int:user_id>', methods=['PUT'])
def update_person(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({'Fetch Error Message': 'Person not found'}), 404

    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if name is not None:
        person.name = name
    if age is not None:
        person.age = age

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
        It provides a simple interface to manage information about individuals, including their names and ages.
        '''})

if __name__ == '__main__':
    create_database()
    port = int(os.environ.get('PORT', 8000))
    debug = bool(os.environ.get('DEBUG', False))
    app.run(host='0.0.0.0', port=port)
