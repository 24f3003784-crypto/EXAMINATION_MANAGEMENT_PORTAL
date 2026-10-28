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
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='student_profile')

class Examiner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True) 
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True) 
    contact_info = db.Column(db.String(255), nullable=True) 
    approval_status = db.Column(db.String(20), nullable=False, default='Pending') # 'Pending', 'Approved', 'Rejected'
    is_suspended = db.Column(db.Boolean, nullable=False, default=False) 
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('User',back_populates='examiner_profile')
    department = db.relationship('Department', back_populates='examiner')
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.now(timezone.utc))
    

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String(255), nullable=False)
    department_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.now(timezone.utc))
    
    examiner = db.relationship('Examiner', back_populates='department')