from app import create_app
from app import seed_admin,seed_departments
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_admin()
        seed_departments()
    app.run(debug=True)