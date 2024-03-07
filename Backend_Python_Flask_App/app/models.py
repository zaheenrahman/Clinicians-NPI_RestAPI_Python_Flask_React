from app import db

class Clinician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    npi_number = db.Column(db.String(10), unique=True, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    appointments = db.relationship('Appointment', backref='clinician', lazy='dynamic')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)  # Date of Birth
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey('clinician.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    status = db.Column(db.String(64), nullable=False)