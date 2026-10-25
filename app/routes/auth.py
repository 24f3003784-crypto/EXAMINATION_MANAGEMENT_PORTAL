from flask import Blueprint,flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user,logout_user, login_required,UserMixin
from app.models import User, Student, Examiner, Examination, Course
from app.extensions import db
auth = Blueprint('auth', __name__)

def redirect_for_role(user):
    """Send each role to its own dashboard after login."""
    if user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    if user.role == "student":
        return redirect(url_for("student.dashboard"))
    if user.role == "examiner":
        return redirect(url_for("examiner.dashboard"))
    
    flash("Your account role is not recognized.", "danger")
    return redirect(url_for("main.index"))


def find_user_by_email(email):
    """Normalize email lookup so registration and login behave consistently."""
    return User.query.filter_by(email=email.strip().lower()).first()


def is_valid_email(email):
    """Tiny beginner-friendly email check."""
    return "@" in email and "." in email.split("@")[-1]

@auth.route('/login',methods=['GET', 'POST'])
def login():
     if current_user.is_authenticated:
        return redirect_for_role(current_user)

     if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = find_user_by_email(email)

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        if not user.is_active or user.is_blacklisted:
            flash("This account is not allowed to log in. Please contact support.", "danger")
            return render_template("auth/login.html")

        if user.role == "examiner":
            examiner = user.Examiner_profile
            if not examiner:
                flash("Examiner profile is missing. Please contact support.", "danger")
                return render_template("auth/login.html")
            if examiner.approval_status != "approved":
                flash("Your examiner account is still awaiting admin approval.", "warning")
                return render_template("auth/login.html")
            if examiner.is_suspended:
                flash("Your examiner account is suspended.", "danger")
                return render_template("auth/login.html")

        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect_for_role(user)
    
     return render_template("auth/login.html")   

@auth.route('/register/student')
def register_student():
    return render_template('/auth/register_student.html')

@auth.route('/register/examiner')
def register_examiner():
    return render_template('/auth/register_examiner.html')

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    """End the current login session."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))