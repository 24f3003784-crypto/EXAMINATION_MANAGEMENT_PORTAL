from flask import Blueprint,render_template, redirect, url_for,flash 
from flask_login import current_user, login_required

from app.extensions import db
from app.models import User, Student, Examiner, Course

admin_bp= Blueprint('admin', __name__, url_prefix="/admin")


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/examiners')
@login_required
def examiners():
    pending_examiners = Examiner.query.filter_by(approval_status='Pending').all()
    approved_examiners = Examiner.query.filter_by(approval_status='Approved').all()
    return render_template('/admin/examiners.html', pending_examiners=pending_examiners, approved_examiners=approved_examiners)

@admin_bp.route('/students')
@login_required 
def students():
    students = Student.query.all()
    return render_template('/admin/students.html', students=students)

@admin_bp.route('/approve_examiner/<int:examiner_id>', methods=['POST'])
@login_required
def approve_examiner(examiner_id):
    examiner = Examiner.query.get(examiner_id)
    if examiner:
        examiner.approval_status = 'Approved'
        db.session.commit()
        flash(f"Examiner {examiner.user.name} has been approved.", "success")
    else:
        flash("Examiner not found.", "danger")
    return redirect(url_for('admin.examiners'))

@admin_bp.route('/reject_examiner/<int:examiner_id>', methods=['POST'])
@login_required 
def reject_examiner(examiner_id):
    examiner = Examiner.query.get(examiner_id)
    if examiner:
        examiner.approval_status = 'Rejected'
        db.session.commit()
        flash(f"Examiner {examiner.user.name} has been rejected.", "success")
    else:
        flash("Examiner not found.", "danger")
    return redirect(url_for('admin.examiners'))

@admin_bp.route('/blacklist/<int:examiner_id>', methods=['POST'])
@login_required
def toggle_blacklist_examiner(examiner_id):
    examiner = Examiner.query.get(examiner_id)
    examiner.user.is_blacklisted = not examiner.user.is_blacklisted
    db.session.commit()
    flash('Status updated', "success")
    return redirect(url_for('admin.examiners'))