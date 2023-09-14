# Tipsy API for Managing People Records
This API is designed to perform CRUD operations on a database of people records.
It provides a simple interface to manage information about individuals, including their names and ages.

# Table of Contents

- Getting Started
  - Features
  - Prerequisites
  - Installation
- Running the API 
- Using the API
  - API Endpoints
- License


## Getting Started
## Features
- Create a new person record.
- Read details of a person by their ID.
- Update the details of an existing person by their ID.
- Delete a person record by their ID.
- Handle database integrity errors gracefully.

## Prerequisites
Before running the API, make sure you have the following installed:
- Python
- Flask
- Flask-SQLAlchemy
- SQLite 
- Postman (for testing)

## Installation
1. Clone or download this repository to your local machine.
2. Navigate to the project directory.
3. Initialize the database.
4. Run the API:
python project.py

The API should now be running locally at `http://localhost:5000`.

## Using the API
API Endpoints

- **POST /api**: Add a new person to the database. Send a JSON request with the person's name and age.
- **GET /api/<int:user_id>**: Retrieve details of a person by their ID.
- **PUT /api/<int:user_id>**: Update details of an existing person by their ID. Send a JSON request with the new name and/or age.
- **DELETE /api/<int:user_id>**: Remove a person by their ID.



# Create a Person

- **URL:** `/api`
- **Method:** `POST`
- **Request Body:** JSON data

Open Postman
Create a New Request.
Select the Request Type:
In the request window, select the request type as "POST" 
Enter the API URL:
	http://localhost:5000/api

Set Headers:
Add a header with the key "Content-Type" and the value "application/json". 
This tells the API that you are sending JSON data.

Enter JSON Data:
Click on the "Body" tab below the URL field.
Select the "raw" option.
In the dropdown next to "raw," select "JSON (application/json)".
  
  [
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
    }
  ]

Response:
{
  "Successful Response Message": "Persons added successfully"
}

# Get a Person by ID

- **URL:** `/api/{person_id}`
- **Method:** `GET`

Open Postman
Create a new request.
Set up the GET request:
Define the request URL:
Enter the URL for your Flask API endpoint, including the <user_id> parameter.
For example, if you want to fetch details for a person with ID 1, the URL would be http://127.0.0.1:5000/api/1.
Click the "Send" button to execute the GET request.

## Get All People

- **URL:** `/api`
- **Method:** `GET`
 the URL would be http://127.0.0.1:5000/api


# Update a Person by ID

-**URL:** `/api/{person_id}`
- **Method:**: PUT

1. Open Postman.
2. Create a new request.
3. Select the request type as "PUT".
4. Define the request URL:
   - Enter the URL for your Flask API endpoint.
5. Set the request body:
   - Click on the "Body" tab below the URL field.
   - Select the "raw" option.
   - Choose "JSON (application/json)" 
   - In the text area below, enter the JSON data containing the update info
6. Click the "Send" button to execute the PUT request.

{
  "Update message": "Person updated successfully"
}

# Delete a Person by ID
URL: /api/{person_id}
Method: DELETE


Response:
{
  "Delete message": "Person deleted successfully"
}
}

# Sample Data
[
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
  },
  {
    "name": "Chinedu Okoro",
    "age": 28,
    "gender": "Male",
    "email": "chinedu.okoro28@yahoo.com",
    "phone_number": "09012342567",
    "job": "Engineer"
  },
  {
    "name": "Ama Mensah",
    "age": 30,
    "gender": "Female",
    "email": "ama.mensahanalyst@gmail.com",
    "phone_number": "08026543210",
    "job": "Business Analyst"
  },
  {
    "name": "Obinna Eze",
    "age": 25,
    "gender": "Male",
    "email": "obinna.eze@example.com",
    "phone_number": "555-555-5555",
    "job": "Marketer"
  },
  {
    "name": "Kwame Boateng",
    "age": 32,
    "gender": "Male",
    "email": "kwame.boateng@example.com",
    "phone_number": "111-222-3333",
    "job": "Doctor"
  }
]

License
This project is licensed under the MIT License - see the LICENSE file for details.
