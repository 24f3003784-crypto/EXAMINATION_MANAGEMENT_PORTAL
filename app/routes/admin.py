from flask import Blueprint,render_template, redirect, url_for
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
    examiners = Examiner.query.all()
    return render_template('admin/examiners.html', examiners=examiners)

@admin_bp.route('/approve_examiner/<int:examiner_id>', methods=['POST'])
@login_required
def approve_examiner(examiner_id):
    examiner = Examiner.query.get_or_404(examiner_id)
    examiner.approval_status = 'Approved'
    db.session.commit()
    return redirect(url_for('admin.examiners'))

@admin_bp.route('/reject_examiner/<int:examiner_id>', methods=['POST'])
@login_required 
def reject_examiner(examiner_id):
    examiner = Examiner.query.get_or_404(examiner_id)
    examiner.approval_status = 'Rejected'
    db.session.commit()
    return redirect(url_for('admin.examiners'))