from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, User, Flight, Booking
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password%401@localhost:3306/my_bookings'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

#to register for the user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    name = data['name']
    email = data['email']
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'Username or Email already exists'}), 400
    new_user = User(username=username, password=password, name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

#to login we use username,password.
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful', 'userId': user.id}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


#to add the flight details 

@app.route('/flights', methods=['POST'])
def add_flight():
    data = request.json
    source = data['source']
    flight_number = data['flight_number']
    flight_name = data['flight_name']
    destination = data['destination']
    date = data['date']
    departure_time = data['departure_time']
    arrival_time = data['arrival_time']
    cost = data['cost']
    new_flight = Flight(
        source=source,
        flight_number=flight_number,
        flight_name=flight_name, 
        destination=destination, 
        date=datetime.strptime(date, '%d-%m-%Y').date(), 
        departure_time=departure_time, 
        arrival_time=arrival_time,
        cost=cost

    )
    db.session.add(new_flight)
    db.session.commit()
    return jsonify({'message': 'Flight added successfully'}), 201

#to check the flight details for given source,destination,date

@app.route('/flights', methods=['GET'])
def get_flights():
    source = request.args.get('source')
    destination = request.args.get('destination')
    date = request.args.get('date')

    if not source or not destination:
        return jsonify({'error': 'Source and destination are required fields'}), 400

    query = Flight.query.filter_by(source=source, destination=destination)

    if date:
        query = query.filter_by(date=datetime.strptime(date, '%Y-%m-%d').date())

    flights = query.all()
    if not flights:
        return jsonify({'message': 'No flights available for the selected criteria'}), 404

    flights_list = [
        {
            'id': flight.id,
            'source': flight.source,
            'flight_number': flight.flight_number,
            'flight_name' : flight.flight_name,
            'destination': flight.destination,
            'date': flight.date.strftime('%Y-%m-%d'),
            'departure_time': flight.departure_time,
            'arrival_time': flight.arrival_time,
            'cost' : flight.cost
        }
        for flight in flights
    ]
    return jsonify(flights_list), 200

#to book the flight details we use user_id and flight_id here

@app.route('/book', methods=['POST'])
def book_flight():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401
    
    flight_id = data.get('flight_id')
    if not flight_id:
        return jsonify({'message': 'Flight ID is required'}), 400
    
    booking = Booking(user_id=user_id, flight_id=flight_id)
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'message': 'Flight booked successfully'}), 201

#to get the bookings of the user 

@app.route('/bookings', methods=['GET'])
def get_bookings():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user_id provided in query parameter'}), 400
    
    try:
        bookings = db.session.query(Booking, Flight).join(Flight, Booking.flight_id == Flight.id).filter(Booking.user_id == user_id).all()
        bookings_list = [
            {
                'id': booking.Booking.id,
                'flight_number': booking.Flight.flight_number,
                'flight_name': getattr(booking.Flight, 'flight_name', 'N/A'),  # Use getattr to avoid AttributeError
                'source': booking.Flight.source,
                'destination': booking.Flight.destination,
                'date': booking.Flight.date.strftime('%Y-%m-%d'),
                'cost': booking.Flight.cost
            }
            for booking in bookings
        ]
        return jsonify(bookings_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# to update the booking we use flight_number.

@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    flight_number = data.get('flight_number')
    if not flight_number:
        return jsonify({'message': 'Flight number is required'}), 400

    # Find the flight by flight number
    flight = Flight.query.filter_by(flight_number=flight_number).first()
    if not flight:
        return jsonify({'message': 'Flight not found'}), 404

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    booking.flight_id = flight.id
    db.session.commit()

    return jsonify({'message': 'Booking updated successfully'}), 200
    
# to delete the flight

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)