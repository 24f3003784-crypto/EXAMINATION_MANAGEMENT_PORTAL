from flask import Blueprint,render_template, redirect, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import User, Student, Examiner, Course

student_bp= Blueprint('student', __name__, url_prefix="/student")

@student_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('student/dashboard.html')