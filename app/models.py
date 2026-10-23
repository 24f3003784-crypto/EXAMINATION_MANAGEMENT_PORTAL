from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    d = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    # created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    