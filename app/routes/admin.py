from flask import Blueprint,render_template, redirect, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import User, Student, Examiner, Examination, Course

admin_bp= Blueprint('admin', __name__, url_prefix="/admin")


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')