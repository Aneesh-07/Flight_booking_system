#auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Admin,Flight,Booking
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth,db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        admin_user = Admin.query.filter_by().first()
        if not admin_user:
            default_admin = Admin(email = "aneeshtripathi@gmail.com",password = generate_password_hash("Aneesh@123",method='sha256'))
            db.session.add(default_admin)
            db.session.commit()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    

        admin_user = Admin.query.filter_by(email=email).first()
        if admin_user:
            if check_password_hash(admin_user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(admin_user, remember=True)
                return redirect(url_for('views.admin_panel'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("admin_login.html",user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        gender = request.form.get('gender')
        address = request.form.get('address')
        country = request.form.get('country')
        dob = request.form.get('dob')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                gender=gender,
                address=address,
                country=country,
                dob=dob,
                password=generate_password_hash(password1, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/add-flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        flight_number = request.form.get('flightNumber')
        source = request.form.get('source')
        destination = request.form.get('destination')
        date = request.form.get('date')
        departure_time = request.form.get('departureTime')

        # Create a new Flight object and add it to the database
        new_flight = Flight(
            flight_number=flight_number,
            source=source,
            destination=destination,
            date=date,
            departure_time=departure_time
        )
        db.session.add(new_flight)
        db.session.commit()

        # Redirect to the admin panel or a success page
        return redirect('/admin_panel')

    return render_template("add_flight.html")

@auth.route('/view-bookings', methods=['POST'])
def view_bookings():
    if request.method == 'POST':
        flight_number = request.form.get('flightNumberToView')
        date = request.form.get('dateToView')
        departure_time = request.form.get('departureTimeToView')

        # Query the Flight table to get the matching flights
        flights = Flight.query.filter_by(flight_number=flight_number, date=date, departure_time=departure_time).all()

        # Now you can use the 'flights' list to display the bookings for the specific flight

        return render_template("view_bookings.html", flights=flights)

    return redirect('/admin_panel')

# @auth.route('/search-results', methods=[ 'POST'])
# @login_required
# def search_results():
#     if request.method == 'POST':
#         source = request.form['source']
#         destination = request.form['destination']
#         date = request.form.get('date')
#         time = request.form.get('Time')

#         # Fetch flights based on the search criteria
#         flights = Flight.query.filter_by(source=source, destination=destination, date=date, departure_time=time).all()
#         return render_template('search_results.html', flights=flights)

#     return redirect(url_for('search_flights'))

@auth.route('/book-flight/<int:flight_id>', methods=['GET', 'POST'])
@login_required
def book_flight(flight_id):
    print("hhh1")
    # flight = Flight.query.filter_by(id=flight_id).all()
    flight = Flight.query.get_or_404(flight_id)


    if flight.seats_available > 0:
        print("hhh12")
        # Create a new booking for the current user
        booking = Booking(user_id=current_user.id, flight_id=flight.id)
        flight.seats_available -= 1
        
        
        print("hhh12")
        db.session.add(booking)
        db.session.commit()
        flash('Flight booked successfully!', 'success')
      
        
        

        return redirect(url_for('views.home'))
    else:
        flash('Sorry, the flight is fully booked.', 'error')
        return redirect(url_for('views.home'))
    

@auth.route('/remove-flight', methods=['POST'])
def remove_flight():
    flight_number_to_remove = request.form.get('flightNumberToRemove')
    flight = Flight.query.filter_by(flight_number=flight_number_to_remove).first()

    if flight:
        try:
            db.session.delete(flight)
            db.session.commit()
            flash('Flight removed successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while removing the flight.', 'error')
    else:
        flash('Flight not found. Please enter a valid flight number.', 'error')

    return redirect(url_for('views.home'))
