from flask import Blueprint

view = Blueprint('view', __name__)


@view.route('/about')
def about():
    return '<h1>About Us</h1>'