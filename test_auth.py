import json
import pytest
from Program1 import db, User, Booking

def test_register(test_client):
    # Test successful registration
    response = test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'name': 'Test User',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'
    # Test registration with existing username
    response = test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'name': 'Test User',
        'email': 'testuser2@example.com'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Username or Email already exists'
    # Test registration with existing email
    response = test_client.post('/register', json={
        'username': 'testuser2',
        'password': 'testpassword',
        'name': 'Test User',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Username or Email already exists'
def test_login(test_client):
    # Register a user first
    test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'name': 'Test User',
        'email': 'testuser@example.com'
    })
    # Test successful login
    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'
    assert 'userId' in response.json
    # Test login with incorrect username
    response = test_client.post('/login', json={
        'username': 'wronguser',
        'password': 'testpassword'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password'
    # Test login with incorrect password
    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password'
def test_add_flight(test_client):
    # Test adding a flight
    response = test_client.post('/flights', json={
        'source': 'Source City',
        'flight_number': 123,
        'flight_name': 'Test Flight',  # Ensure 'flight_name' is included
        'destination': 'Destination City',
        'date': '10-07-2024',  # Make sure to format date as expected by your application
        'departure_time': '10:00 AM',
        'arrival_time': '12:00 PM',
        'cost': 500
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Flight added successfully'
import pytest
from datetime import datetime
from Program1 import app, db, Flight  # Adjust the import according to your file structure
def test_get_flights_no_params(test_client):
    # Test without any query parameters
    response = test_client.get('/flights')
    assert response.status_code == 400
    assert 'error' in response.json
def test_get_flights_missing_params(test_client):
    # Test with missing required parameters (source or destination)
    response = test_client.get('/flights?source=City1')
    assert response.status_code == 400
    assert 'error' in response.json
    response = test_client.get('/flights?destination=City2')
    assert response.status_code == 400
    assert 'error' in response.json
def test_get_flights_valid_params(test_client):
    # Test with valid parameters
    response = test_client.get('/flights?source=City1&destination=City2')
    assert response.status_code == 404
    assert 'message' in response.json  # Assuming no flights match this criteria initially
    # Add test data to the database (assuming Flight table is empty initially)
    flight1 = Flight(
        source='City1',
        flight_number=123,
        flight_name='Test Flight 1',
        destination='City2',
        date=datetime.strptime('2024-07-10', '%Y-%m-%d').date(),
        departure_time='10:00 AM',
        arrival_time='12:00 PM',
        cost=500
    )
    db.session.add(flight1)
    db.session.commit()
    # Test with valid parameters again after adding test data
    response = test_client.get('/flights?source=City1&destination=City2')
    assert response.status_code == 200
    flights = response.json
    assert len(flights) == 1  # Assuming only one flight matches the criteria
    assert flights[0]['source'] == 'City1'
    assert flights[0]['destination'] == 'City2'
    assert flights[0]['flight_name'] == 'Test Flight 1'
    # Test with date parameter
    response = test_client.get('/flights?source=City1&destination=City2&date=2024-07-10')
    assert response.status_code == 200
    flights = response.json
    assert len(flights) == 1  # Assuming only one flight matches the criteria
    assert flights[0]['date'] == '2024-07-10'
    # Test with non-matching date parameter
    response = test_client.get('/flights?source=City1&destination=City2&date=2024-07-11')
    assert response.status_code == 404
    assert 'message' in response.json  # Assuming no flights on that date
    # Add more test cases as needed for edge cases or specific scenarios
def test_book_flight(test_client):
    # Register a user first
    test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'name': 'Test User',
        'email': 'testuser@example.com'
    })
    # Login the user to get userId
    login_response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert login_response.status_code == 200
    user_id = login_response.json['userId']
    response = test_client.post('/book', json={
        'user_id': user_id,
        'flight_id': 1  # Adjust flight_id as per your test case, ensure flight with id=1 exists in the test database
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Flight booked successfully'
    # Test booking without user_id
    response = test_client.post('/book', json={
        'flight_id': 1
    })
    assert response.status_code == 401
    assert response.json['message'] == 'User not logged in'
    # Test booking without flight_id
    response = test_client.post('/book', json={
        'user_id': user_id
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Flight ID is required'


 
   

