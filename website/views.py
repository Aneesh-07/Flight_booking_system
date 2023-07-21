# views.py

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note,Flight,Booking,Admin
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        date = request.form.get('date')
        time = request.form.get('departureTime')

        # Fetch flights based on the search criteria
        flights = Flight.query.filter_by(source=source, destination=destination, date=date, departure_time=time).all()
        return render_template('search_results.html', flights=flights)

    return render_template('search_flights.html')






@views.route('/admin_panel', methods=['GET'])
@login_required  # Ensures that only authenticated admins can access this route
def admin_panel():
    # Check if the current user is an admin
   

    # Get all flights from the database
    flights = Flight.query.all()

    # Get all bookings from the database
    bookings = Booking.query.all()

    return render_template("admin_panel.html",user = current_user, flights=flights, bookings=bookings)

@views.route('/my-bookings')
@login_required
def my_bookings():
    # Get all the bookings for the current user
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_booking.html', bookings=bookings)
# @views.route('/book-flight/<int:flight_id>', methods=['GET', 'POST'])
# @login_required
# def book_flight(flight_id):
#     print("hhh1")
#     flight = Flight.query.filter_by(id=flight_id).all()

#     if flight[0].seats_available > 0:
#         print("hhh12")
#         # Create a new booking for the current user
#         booking = Booking(user_id=current_user.id, flight_id=flight[0].id)
#         flight[0].seats_available -= 1

#         try:
#             print("hhh12")
#             db.session.add(booking)
#             db.session.commit()
#             flash('Flight booked successfully!', 'success')
#         except Exception as e:
#             print("hhh12")
#             db.session.rollback()
#             flash('An error occurred while booking the flight.', 'error')

#         return redirect(url_for('views.home'))
#     else:
#         flash('Sorry, the flight is fully booked.', 'error')
#         return redirect(url_for('views.home'))





