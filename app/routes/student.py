from datetime import date
from os import name

from flask import Blueprint,render_template, redirect, request, url_for,abort, flash
from flask_login import current_user, login_required

from app.extensions import db
from app.models import User, Student, Examiner, Course, Booking, ExaminationSlot

student_bp= Blueprint('student', __name__, url_prefix="/student")

@student_bp.route('/dashboard')
@login_required
def dashboard():
    student = current_user.student_profile

    if not student:
        abort(403)

    # Get all currently booked slot IDs for this student
    booked_slot_ids = {
        booking.slot_id
        for booking in student.bookings
        if booking.status == 'Booked'
    }

    # Available examination slots
    available_slots = ExaminationSlot.query.filter(
        ExaminationSlot.status == 'Available',
        ExaminationSlot.available_seats > 0
    ).all()
    return render_template('student/dashboard.html',student=student,available_slots=available_slots,booked_slot_ids=booked_slot_ids)

@student_bp.route('/my_exams')
@login_required
def my_exams():

    student = current_user.student_profile

    if not student:
        abort(403)

    # Get all currently booked slot IDs for this student
    booked_slot_ids = {
        booking.slot_id
        for booking in student.bookings
        if booking.status == 'Booked'
    }

    # Available examination slots
    available_slots = ExaminationSlot.query.filter(
        ExaminationSlot.status == 'Available',
        ExaminationSlot.available_seats > 0
    ).all()

    # Upcoming examinations booked by the student
    upcoming_bookings = Booking.query.join(
        ExaminationSlot,
        Booking.slot_id == ExaminationSlot.id
    ).filter(
        Booking.student_id == student.id,
        Booking.status == 'Booked',
        ExaminationSlot.slot_date == date.today()
    ).order_by(
        ExaminationSlot.slot_date,
        ExaminationSlot.start_time
    ).all()

    # Completed examination bookings
    examination_history = Booking.query.filter_by(
        student_id=student.id,
        status='Completed'
    ).all()

    return render_template(
        'student/my_exam.html',
        student=student,
        available_slots=available_slots,
        booked_slot_ids=booked_slot_ids,
        upcoming_bookings=upcoming_bookings,
        examination_history=examination_history
    )

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():  
    student = current_user.student_profile
    return render_template('student/profile.html', student=student)

@student_bp.route('/update', methods=['POST'])
@login_required
def update_student_profile():
    
    print("UPDATE STUDENT PROFILE ROUTE REACHED")

    student = current_user.student_profile

    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()

    # Validate inputs
    if not name or not email:
        flash('Name and email are required.', 'danger')
        return redirect(url_for('student.profile'))

    # Check whether email is already registered
    existing_user = User.query.filter(
        User.email == email,
        User.id != current_user.id
    ).first()

    if existing_user:
        flash('This email is already registered.', 'danger')
        return redirect(url_for('student.profile'))

    try:
        # Update User table
        current_user.name = name
        current_user.email = email

        # Synchronize Student table
        student.name = name

        db.session.commit()

        flash('Profile updated successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        print("Profile update error:", e)
        flash('Unable to update profile. Please try again.', 'danger')

    return redirect(url_for('student.profile'))

@student_bp.route('/bookings')
@login_required
def bookings():
    student = current_user.student_profile

    if not student:
        abort(403)

    # Get all bookings for the student
    bookings = Booking.query.filter_by(student_id=student.id).all()

    return render_template('student/my_bookings.html', student=student, bookings=bookings)

@student_bp.route('/book_slot/<int:slot_id>', methods=['POST'])
@login_required
def book_slot(slot_id):
    student = current_user.student_profile

    if not student:
        abort(403)

    slot = ExaminationSlot.query.get_or_404(slot_id)

    # Check if the student has already booked this slot
    existing_booking = Booking.query.filter_by(student_id=student.id, slot_id=slot.id).first()
    if existing_booking:
        flash('You have already booked this slot.', 'warning')
        return redirect(url_for('student.dashboard'))

    # Check if the slot is available and has seats
    if slot.status != 'Available' or slot.available_seats <= 0:
        flash('This slot is not available for booking.', 'danger')
        return redirect(url_for('student.dashboard'))

    # Create a new booking
    new_booking = Booking(student_id=student.id, slot_id=slot.id)
    db.session.add(new_booking)

    # Decrease the available seats for the slot
    slot.available_seats -= 1
    if slot.available_seats == 0:
        slot.status = 'Full'

    db.session.commit()
    flash('Slot booked successfully!', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    student = current_user.student_profile

    if not student:
        abort(403)

    booking = Booking.query.get_or_404(booking_id)

    # Ensure the booking belongs to the current student
    if booking.student_id != student.id:
        abort(403)

    # Update the booking status to 'Cancelled'
    booking.status = 'Cancelled'

    # Increase the available seats for the slot
    slot = booking.slot
    slot.available_seats += 1
    if slot.status == 'Full':
        slot.status = 'Available'

    db.session.commit()
    flash('Booking cancelled successfully!', 'success')
    return redirect(url_for('student.my_exams'))

@student_bp.route('/results')
@login_required
def results():
    student = current_user.student_profile

    if not student:
        abort(403)

    # Get all completed bookings for the student
    completed_bookings = Booking.query.filter_by(student_id=student.id, status='Completed').all()

    return render_template('student/view_results.html', student=student, completed_bookings=completed_bookings)

@student_bp.route('/view_results/<int:booking_id>')
@login_required
def view_results(booking_id):
    student = current_user.student_profile

    if not student:
        abort(403)

    booking = Booking.query.get_or_404(booking_id)

    # Ensure the booking belongs to the current student
    if booking.student_id != student.id:
        abort(403)

    # Ensure the booking is completed before viewing results
    if booking.status != 'Completed':
        flash('Results are not available for this booking yet.', 'warning')
        return redirect(url_for('student.my_exams'))

    evaluations = booking.evaluations

    return render_template('student/view_results.html', student=student, booking=booking, evaluations=evaluations)