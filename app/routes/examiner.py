from flask import Blueprint,render_template, redirect, url_for,flash 
from flask_login import current_user, login_required

from app.extensions import db
from app.models import User, Student, Examiner, Course

examiner_bp= Blueprint('examiner', __name__, url_prefix="/examiner")

@examiner_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('examiner/dashboard.html')