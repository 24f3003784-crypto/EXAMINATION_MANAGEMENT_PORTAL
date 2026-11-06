from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    #Relationships
    examiner_profile = db.relationship('Examiner', back_populates='user', uselist=False)
    student_profile = db.relationship('Student', back_populates='user', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)   
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    roll_number = db.Column(db.String(50), nullable=True) # Add this line
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='student_profile')
    bookings = db.relationship('Booking', back_populates='student', cascade='all, delete-orphan')

class Examiner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True) 
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True) 
    contact_info = db.Column(db.String(255), nullable=True) 
    approval_status = db.Column(db.String(20), nullable=False, default='Pending') # 'Pending', 'Approved', 'Rejected'
    is_suspended = db.Column(db.Boolean, nullable=False, default=False) 
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('User',back_populates='examiner_profile')
    department = db.relationship('Department', back_populates='examiners')
    slots = db.relationship('ExaminationSlot', back_populates='examiner')
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True) 
    status = db.Column(db.String(20), nullable=False, default='Active')
    created_at = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.now(timezone.utc))
    
    examinations = db.relationship('Examination', back_populates='course', cascade='all, delete-orphan')

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String(255), nullable=False)
    department_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.now(timezone.utc))
    
    examiners = db.relationship('Examiner', back_populates='department')
    
class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    examination_name = db.Column(db.String(255), nullable=False)
    examination_type = db.Column(db.String(50), nullable=False) # Viva, Practical, Project Demo, Assessment
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    max_marks = db.Column(db.Float, nullable=False, default=100.0) 
    # Timelines enforced by Python comparisons
    
    slot_creation_start = db.Column(db.DateTime, nullable=True)
    slot_creation_end = db.Column(db.DateTime, nullable=True)
    slot_booking_start = db.Column(db.DateTime, nullable=True)
    slot_booking_end = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.String(30), nullable=False, default='Draft') # Draft, Slot Creation, Booking Open, Closed, Completed
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    # Relationships
    course = db.relationship('Course', back_populates='examinations')
    rubrics = db.relationship('ExaminationRubric', back_populates='examination', cascade='all, delete-orphan') 
    slots = db.relationship('ExaminationSlot', back_populates='examination', cascade='all, delete-orphan')

class ExaminationRubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    criterion_name = db.Column(db.String(255), nullable=False)
    max_marks = db.Column(db.Float, nullable=False)
    weightage = db.Column(db.Float, nullable=True, default=1.0)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    examination = db.relationship('Examination', back_populates='rubrics')
    evaluations = db.relationship('Evaluation', back_populates='rubric')

class ExaminationSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiner.id'), nullable=False)
    slot_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False, default=1)
    available_seats = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(20), nullable=False, default='Available')  # Available, Full, Cancelled, Completed

    # Relationships
    examination = db.relationship('Examination', back_populates='slots')
    examiner = db.relationship('Examiner', back_populates='slots')
    bookings = db.relationship('Booking', back_populates='slot', cascade='all, delete-orphan')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('examination_slot.id'), nullable=False)
    booking_date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default='Booked')  # Booked, Cancelled, Completed

    # Relationships
    student = db.relationship('Student', back_populates='bookings')
    slot = db.relationship('ExaminationSlot', back_populates='bookings')
    evaluations = db.relationship('Evaluation', back_populates='booking', cascade='all, delete-orphan')

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer,	db.ForeignKey('booking.id'),	nullable=False)
    rubric_id =	db.Column(db.Integer,	db.ForeignKey('examination_rubric.id'),	nullable=False)
    marks_obtained =	db.Column(db.Float,	nullable=False)
    remarks =	db.Column(db.Text,	nullable=True)
    evaluated_at =	db.Column(db.DateTime(timezone=True),	nullable=False,	default=lambda: datetime.now(timezone.utc))

    # Relationships
    booking =	db.relationship('Booking',	back_populates='evaluations')
    rubric =	db.relationship('ExaminationRubric',back_populates='evaluations')
