# Patient Management System API

## Overview
This project is part of the backend development for an internal tool designed to manage patients and their appointments. It serves as a REST API built with Flask, a Python web framework, and utilizes SQLite as the database for storing data. The API manages three main resources: clinicians, patients, and appointments, facilitating the creation, reading, updating, and deletion (CRUD) of these resources.

## Project Setup

### Requirements
- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- SQLite
- Requests

### Installation

1. Clone the repository: git clone!

2. Navigate to the project directory: cd main

3. Install the required packages: pip install -r requirements.txt

4. Initialize the database:

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

Start the application:
flask run

## API Endpoints

### Clinicians

- **POST /clinicians**: Add a new clinician. Validates the NPI number against external API.
- **GET /clinicians**: Retrieve all clinicians.
- **GET /clinicians/<clinician_id>**: Retrieve a clinician by ID.
- **PUT /clinicians/<clinician_id>**: Update a clinician's information.
- **DELETE /clinicians/<clinician_id>**: Delete a clinician by ID.

### Patients

- **POST /patients**: Add a new patient.
- **GET /patients**: Retrieve all patients.
- **GET /patients/<patient_id>**: Retrieve a patient by ID.
- **PUT /patients/<patient_id>**: Update a patient's information.
- **DELETE /patients/<patient_id>**: Delete a patient by ID.

### Appointments

- **POST /appointments**: Schedule a new appointment.
- **GET /appointments**: Retrieve all appointments, with optional filters.
- **GET /appointments/<appointment_id>**: Retrieve an appointment by ID.
- **PUT /appointments/<appointment_id>**: Update an appointment's details.
- **DELETE /appointments/<appointment_id>**: Cancel an appointment.

### File Comments ###

---
__init__.py - Application Initialization
This file serves as the entry point for the Flask application. It is responsible for setting up the core components needed for the application to run smoothly. Below is a breakdown of its key components:

Flask Application Instance: The app variable is an instance of the Flask class. This is the central object in your Flask application. It is used to handle all the requests and responses.

Configuration: The application loads its configuration settings from the Config class located in the config.py file. This includes configurations like the database URI, secret key, and any other environment-specific settings.

Cross-Origin Resource Sharing (CORS): By calling CORS(app), the application is configured to allow cross-origin requests from any domain. This is particularly useful for APIs consumed by web applications hosted on different domains.

SQLAlchemy Setup: db is an instance of SQLAlchemy, a database toolkit and ORM that provides full power and flexibility of SQL. It is linked to the Flask app for database operations.

Flask-Migrate for Database Migrations: migrate is an instance of Migrate, integrating Alembic (a database migration tool) with the application. It is used for creating and managing database schema migrations.

Model and View Imports: The application imports models and views from the app package. Models define the database schema, while views handle the routing and logic of the application.

Root Route: A simple root route (/) is defined that returns a plain text response. This can be used as a basic health check or welcome message for the application.
---

## **models.py** 

Models Overview

Clinician Model
Purpose: Represents healthcare clinicians within the system.

Fields:
id: A unique identifier for each clinician. It serves as the primary key.
first_name and last_name: The clinician's first and last names. Both are indexed to improve query performance on these fields.
npi_number: The National Provider Identifier (NPI), a unique 10-digit identification number for covered healthcare providers in the United States. It's marked as unique, ensuring no two clinicians have the same NPI.
state: The state in which the clinician is registered to practice. This is stored as a 2-letter code and is marked as unique, which might be a mistake since multiple clinicians can practice in the same state.
appointments: A dynamic relationship to the Appointment model. This allows for querying a clinician's appointments directly from a clinician instance.

Patient Model
Purpose: Represents patients within the system.

Fields:
id: A unique identifier for each patient, serving as the primary key.
first_name and last_name: The patient's first and last names, both indexed for improved query performance.
dob: The date of birth of the patient, essential for medical records and age calculation.
appointments: A dynamic relationship to the Appointment model, facilitating the querying of a patient's appointments directly.

Appointment Model
Purpose: Manages the appointments between clinicians and patients.

Fields:
id: A unique identifier for each appointment, serving as the primary key.
appointment_date: The date and time when the appointment is scheduled to take place.
clinician_id: A foreign key linking to the Clinician model, indicating which clinician is associated with the appointment.
patient_id: A foreign key linking to the Patient model, indicating which patient the appointment is for.
status: The status of the appointment (e.g., scheduled, cancelled, completed), allowing for the management of appointment lifecycle.

Relationships
The Clinician and Patient models are linked to the Appointment model via foreign keys, establishing a one-to-many relationship from clinicians and patients to appointments. This means a single clinician or patient can have multiple associated appointments. The backref in each relationship provides a simple way to access related appointments from a clinician or patient instance.

#### *Notes*

The uniqueness constraint on the state field in the Clinician model might need to be revisited, as typically multiple clinicians would practice in the same state.

The dynamic loading strategy (lazy='dynamic') for the appointments relationships allows for more flexible and efficient querying of related appointments, as it returns a query object instead of a list of items.

This file is crucial for the application's data layer, defining how data is structured and stored in the database.

---
## **Utils.py - Validate_npi Functionality**
The primary purpose of the validate_npi function is to ensure the integrity and correctness of the NPI number provided for clinicians being added to or updated in the system. It leverages the external NPI registry API to cross-verify the NPI number against the clinician's personal and professional details.

Functionality
Arguments: The function takes four string arguments: npi_number, first_name, last_name, and state. These represent the NPI number to be validated and the clinician's first name, last name, and state of practice, respectively.

Process:
Constructs a request to the NPI registry API with the provided details.
Sends the request and waits for the response from the API.
Checks the response status code for any HTTP errors and raises an exception if any are found.
Parses the JSON response to check the result_count. A result_count greater than 0 indicates that the NPI number is valid and matches the provided details.

Returns: The function returns a boolean value, True if the NPI number is valid and matches the clinician's details according to the NPI registry, and False otherwise.

Error Handling
The function uses a try-except block to catch and handle any exceptions raised due to request issues (like network problems or invalid responses from the API). This ensures that the function gracefully handles errors and simply returns False if the validation cannot be completed due to external factors.

Usage
This utility function is likely called when clinicians are added or their details are updated in the system, providing an additional layer of data validation to ensure the accuracy and validity of clinician records.

Notes
The commented-out limit parameter in the params dictionary suggests there was consideration to limit the number of results returned by the API. However, it's left commented and thus not in use, which might affect performance for queries that could return a large number of matches. Including this parameter with a small value (like 1) could potentially improve response times and reduce data processing overhead. As this project is utilizing small datasets it is not used and left commented out.

---

## **Views.py - Routing**

This file leverages Flask's capabilities to define endpoints for creating, retrieving, updating, and deleting resources in a RESTful manner. It makes extensive use of request to access the data sent by clients, jsonify to format the response data as JSON, and abort to handle error situations gracefully. The use of the validate_npi utility function for clinician validation adds a layer of data integrity and compliance with external standards. Overall, views.py is designed to provide a comprehensive API for managing clinicians, patients, and appointments within the application.

#Clinicians Management

Add a Clinician

Endpoint: POST /clinicians
Functionality: Validates and adds a new clinician to the database. It ensures that all required fields are provided and validates the NPI number against an external API.

Validation: Checks for the presence of first_name, last_name, npi_number, and state. Additionally, it validates the NPI number for authenticity and match against provided details.
Get All Clinicians

Endpoint: GET /clinicians
Functionality: Retrieves a list of all clinicians stored in the database, returning their details in a JSON format.
Get a Single Clinician

Endpoint: GET /clinicians/<clinician_id>
Functionality: Fetches details of a specific clinician by their ID. Returns a 404 error if the clinician does not exist.
Update a Clinician

Endpoint: PUT /clinicians/<clinician_id>
Functionality: Updates the details of a specific clinician. It also re-validates the NPI number if it's provided in the update.

Delete a Clinician

Endpoint: DELETE /clinicians/<clinician_id>
Functionality: Removes a clinician from the database by their ID. Returns a success message upon deletion.

### Patients Management

Add a Patient

Endpoint: POST /patients
Functionality: Adds a new patient to the database after validating that all required information (first_name, last_name, dob) is provided.

Update a Patient

Endpoint: PUT /patients/<patient_id>
Functionality: Updates the details of an existing patient. It includes handling for the dob field to ensure it's provided in a valid format.

Retrieve Patients

Endpoint: GET /patients and GET /patients/<patient_id>
Functionality: Fetches all patients or a specific patient by their ID, returning their details in a JSON format.

Delete a Patient

Endpoint: DELETE /patients/<patient_id>
Functionality: Deletes a patient from the database, identified by their ID.

#Appointments Management

Add an Appointment

Endpoint: POST /appointments
Functionality: Schedules a new appointment after validating the presence of all required details and ensuring the date is in the correct format.

Retrieve Appointments

Endpoints: GET /appointments and GET /appointments/<appointment_id>
Functionality: Retrieves all appointments or a specific appointment by ID. Supports filtering appointments based on start and end dates.

Update an Appointment

Endpoint: PUT /appointments/<appointment_id>
Functionality: Updates the details of a specific appointment, including date and status. It validates the date format during the update.

Delete an Appointment

Endpoint: DELETE /appointments/<appointment_id>
Functionality: Deletes an appointment by its ID. It includes error handling for any issues that occur during the deletion process.

----

## **Testing Information**

Retrieving Appointments with Filters

Method: GET
URL: http://localhost:5000/appointments?start=2023-12-10T00:00:00&end=2023-12-14T23:59:59

Description: Retrieves appointments within a specific date range.

Retrieving All Appointments

Method: GET
URL: http://127.0.0.1:5000/appointments

Description: Fetches all appointments from the database.

Retrieving All Patients

Method: GET
URL: http://127.0.0.1:5000/patients

Description: Retrieves all patients stored in the system.

Adding a Clinician

Method: POST
URL: http://127.0.0.1:5000/clinicians
Headers: Content-Type: application/json
Body:
json
{
  "first_name": "RAVI",
  "last_name": "ADUSUMILLI",
  "npi_number": "1932102084",
  "state": "OH"
}

Description: Adds a new clinician with the given details to the database.

Adding Another Clinician

Method: POST
URL: http://127.0.0.1:5000/clinicians
Headers: Content-Type: application/json
Body:
json

{
  "first_name": "WILLIAM",
  "last_name": "PILCHER",
  "npi_number": "1588667638",
  "state": "FL"
}

Description: Demonstrates adding another clinician to the system.

Scheduling an Appointment

Method: POST
URL: http://127.0.0.1:5000/appointments
Headers: Content-Type: application/json
Body:
json
{
    "appointment_date": "2023-12-15T14:30:00",
    "clinician_id": 2,
    "patient_id": 3,
    "status": "Scheduled"
}

Description: Schedules a new appointment with the given details.

### *Tips for Testing*

Ensure your Flask application is running locally on port 5000.

For POST requests, set the Content-Type header to application/json and include the request body in JSON format.

For requests that require an ID (like updating or deleting a specific record), ensure the record exists in your database, and use the correct ID in the URL.

Use real NPI numbers for clinician additions to pass the validation (as shown in the examples).

The dates and IDs provided in the requests should be adjusted based on the actual data in your database.

### Misc - Images working preview ###

![image](https://github.com/zaheenrahman/Backend_NPI-RestAPI/assets/35182751/52dc6be2-f743-43b2-b7a5-6c2311c2ebe8)

#### Post request for sample patient
![image](https://github.com/zaheenrahman/Backend_NPI-RestAPI/assets/35182751/6057e307-f481-40e5-a614-b65350f94a2f)

#### Post for Clinicians 
![image](https://github.com/zaheenrahman/Backend_NPI-RestAPI/assets/35182751/6c661eb8-b366-47f6-bd70-fab6ada72909)

#### Appointments Scheduled:

![image](https://github.com/zaheenrahman/Backend_NPI-RestAPI/assets/35182751/0a44c130-45b2-4f2c-b12c-616fc29f452a)





