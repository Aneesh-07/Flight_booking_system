# models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Set nullable to False to enforce email presence
    password = db.Column(db.String(150), nullable=False)  # Set nullable to False to enforce password presence
    first_name = db.Column(db.String(150), nullable=False)  # Set nullable to False to enforce first_name presence
    gender = db.Column(db.String(10), nullable=False)  # Adding gender field (assuming a string field with max length of 10)
    address = db.Column(db.String(200), nullable=True)  # Adding address field (nullable as it might not always be provided)
    country = db.Column(db.String(100), nullable=True)  # Adding country field (nullable as it might not always be provided)
    dob = db.Column(db.String(10), nullable=False)  # Adding dob field (assuming a string field with max length of 10)
    
    def is_authenticated(self):
        return True
    def is_admin(self):
        return False
    


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def is_authenticated(self):
        return True  # For simplicity, consider all admins authenticated after login

    def is_active(self):
        return True  # For simplicity, consider all admins active

    def is_admin(self):
        return True

    
  

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)
    seats_available = db.Column(db.Integer, nullable=True, default=60)



class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=True)
    flight = db.relationship('Flight', backref='bookings')
    
