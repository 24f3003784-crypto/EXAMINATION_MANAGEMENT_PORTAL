from flask import Blueprint, render_template


main_bp = Blueprint("main", __name__)


@main_bp.route("/index")
def index():
    """Render the public landing page."""
    return render_template("index.html")