from flask import request, jsonify, abort
from datetime import datetime
from app import app, db
from app.models import Clinician, Patient, Appointment
from app.utils import validate_npi
from sqlalchemy.orm import joinedload
from sqlalchemy import or_




#----Route for Clinicians----#

#Add and validate clinicians

@app.route('/clinicians', methods=['POST'])
def add_clinician():
    data = request.get_json()
    if not all(key in data for key in ['first_name', 'last_name', 'npi_number', 'state']):
        abort(400)  # Bad request

    # Validate the NPI number
    if not validate_npi(data['npi_number'], data['first_name'], data['last_name'], data['state']):
        return jsonify({"error": "Invalid NPI number or it does not match the provided details"}), 400

    clinician = Clinician(first_name=data['first_name'], last_name=data['last_name'], npi_number=data['npi_number'], state=data['state'])
    db.session.add(clinician)
    db.session.commit()
    return jsonify(clinician.id), 201

#Get All Clinicians

@app.route('/clinicians', methods=['GET'])
def get_clinicians():
    clinicians = Clinician.query.all()
    clinicians_list = []
    for clinician in clinicians:
        clinicians_list.append({
            'id': clinician.id,
            'first_name': clinician.first_name,
            'last_name': clinician.last_name,
            'npi_number': clinician.npi_number,
            'state' : clinician.state
        })
    return jsonify(clinicians_list)

#Get 1 Clinician 

@app.route('/clinicians/<int:clinician_id>', methods=['GET'])
def get_clinician(clinician_id):
    clinician = Clinician.query.get(clinician_id)
    if clinician is None:
        abort(404)  # Not found
    return jsonify({
        'id': clinician.id,
        'first_name': clinician.first_name,
        'last_name': clinician.last_name,
        'npi_number': clinician.npi_number,
        'state' : clinician.state
    })

#Update Clinicians
@app.route('/clinicians/<int:clinician_id>', methods=['PUT'])
def update_clinician(clinician_id):
    clinician = Clinician.query.get_or_404(clinician_id)
    data = request.get_json()

    # Validate the NPI number with possibly updated details
    if not validate_npi(data.get('npi_number', clinician.npi_number),
                        data.get('first_name', clinician.first_name),
                        data.get('last_name', clinician.last_name),
                        data.get('state', clinician.state)):
        return jsonify({"error": "Invalid NPI number or it does not match the provided details"}), 400

    # Update details only if NPI validation is successful
    clinician.first_name = data.get('first_name', clinician.first_name)
    clinician.last_name = data.get('last_name', clinician.last_name)
    clinician.npi_number = data.get('npi_number', clinician.npi_number)
    clinician.state = data.get('state', clinician.state)

    db.session.commit()
    return jsonify({
        'id': clinician.id,
        'first_name': clinician.first_name,
        'last_name': clinician.last_name,
        'npi_number': clinician.npi_number,
        'state': clinician.state
    })

#Delete Clinicians

@app.route('/clinicians/<int:clinician_id>', methods=['DELETE'])
def delete_clinician(clinician_id):
    clinician = Clinician.query.get_or_404(clinician_id)
    db.session.delete(clinician)
    db.session.commit()
    return jsonify({'message': 'Clinician deleted successfully'})

#----Route for Patient----#

#Create (Add)
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    if not data or 'first_name' not in data or 'last_name' not in data or 'dob' not in data:
        return jsonify({'error': 'Missing data'}), 400

    # Parse 'dob' from string to date object
    try:
        dob_date = datetime.strptime(data['dob'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    new_patient = Patient(first_name=data['first_name'], last_name=data['last_name'], dob=dob_date)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'id': new_patient.id, 'first_name': new_patient.first_name, 'last_name': new_patient.last_name, 'dob': new_patient.dob.isoformat()}), 201

#Update 
@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()

    patient.first_name = data.get('first_name', patient.first_name)
    patient.last_name = data.get('last_name', patient.last_name)

    # Handle 'dob' update with date conversion
    if 'dob' in data:
        try:
            patient.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    db.session.commit()
    return jsonify({'id': patient.id, 'first_name': patient.first_name, 'last_name': patient.last_name, 'dob': patient.dob.isoformat()})

#Retrieve
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{'id': patient.id, 'first_name': patient.first_name, 'last_name': patient.last_name, 'dob': patient.dob.isoformat()} for patient in patients])

#Patient by ID
@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({'id': patient.id, 'first_name': patient.first_name, 'last_name': patient.last_name, 'dob': patient.dob.isoformat()})

#Delete
@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'})

#---Route for Appointments---#

#Add Appointment
@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    
    # Check for required fields
    required_fields = ['appointment_date', 'clinician_id', 'patient_id', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required data'}), 400

    try:
        # Parse the appointment date from the provided string
        appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM:SS.'}), 400

    # Create a new Appointment instance
    new_appointment = Appointment(
        appointment_date=appointment_date,
        clinician_id=data['clinician_id'],
        patient_id=data['patient_id'],
        status=data['status']  # Setting the status from the provided data
    )

    db.session.add(new_appointment)
    db.session.commit()

    # Fetch patient's full name for the response
    patient = Patient.query.get(new_appointment.patient_id)
    patient_name = f"{patient.first_name} {patient.last_name}" if patient else "Unknown"

    # Prepare the response data
    appointment_data = {
        'message': 'Appointment added successfully',
        'id': new_appointment.id,
        'appointment_date': new_appointment.appointment_date.isoformat(),
        'clinician_id': new_appointment.clinician_id,
        'patient_id': new_appointment.patient_id,
        'patient_name': patient_name,
        'status': new_appointment.status
    }

    return jsonify(appointment_data), 201

#Retrieve Appointment
@app.route('/appointments', methods=['GET'])
def get_appointments():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    query = Appointment.query
    
    if start_date:
        query = query.filter(Appointment.appointment_date >= start_date)
    if end_date:
        query = query.filter(Appointment.appointment_date <= end_date)
    
    appointments = query.all()

    appointments_list = [{
        'id': appt.id,
        'appointment_date': appt.appointment_date.isoformat(),
        'clinician_id': appt.clinician_id,
        'patient_id': appt.patient_id,
        'patient_name': f"{appt.patient.first_name} {appt.patient.last_name}" if appt.patient else "Unknown",
        'status': appt.status
    } for appt in appointments]

    return jsonify(appointments_list)

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = db.session.query(Appointment).join(Patient, Appointment.patient_id == Patient.id)\
        .filter(Appointment.id == appointment_id).first_or_404()

    return jsonify({
        'id': appointment.id,
        'appointment_date': appointment.appointment_date.isoformat(),
        'clinician_id': appointment.clinician_id,
        'patient_id': appointment.patient_id,
        'patient_name': f"{appointment.patient.first_name} {appointment.patient.last_name}",
        'status': appointment.status
    })

#Update Appointment 
@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()

    if 'appointment_date' in data:
        try:
            appointment.appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM:SS.'}), 400
    
    if 'status' in data:
        appointment.status = data['status']
    
    appointment.clinician_id = data.get('clinician_id', appointment.clinician_id)
    appointment.patient_id = data.get('patient_id', appointment.patient_id)
    
    db.session.commit()

    # Fetch the patient's name for the response
    patient = Patient.query.get(appointment.patient_id)
    patient_name = f"{patient.first_name} {patient.last_name}" if patient else "Unknown"

    return jsonify({
        'message': 'Appointment updated successfully',
        'id': appointment.id,
        'patient_name': patient_name,
        'status': appointment.status
    })

#Delete Appointment
@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'}), 200
    except Exception as e:
        # Log the exception e if logging is set up
        db.session.rollback()  # Roll back the session in case of error
        return jsonify({'error': 'Failed to delete the appointment', 'details': str(e)}), 500