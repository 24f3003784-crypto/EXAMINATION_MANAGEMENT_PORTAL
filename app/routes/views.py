from flask import Blueprint,render_template, redirect, url_for

views= Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    user = "Arjun"
    age =21
    return render_template('home.html',user=user,age=age)

    