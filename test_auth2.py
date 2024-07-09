import pytest
from datetime import datetime
from Program1 import app, db, Flight, Booking
def test_get_bookings(test_client):
    # Register a user first (assuming registration works and user_id is obtained)
    register_response = test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'name': 'Test User',
        'email': 'testuser@example.com'
    })
    assert register_response.status_code == 201

    # Login the user to get userId
    login_response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert login_response.status_code == 200
    user_id = login_response.json['userId']

    # Add some bookings to the database for the logged-in user
    flight1 = Flight(
        flight_number=123,
        flight_name='Test Flight 1',
        source='Source City 1',
        destination='Destination City 1',
        date='2024-07-10',
        departure_time='10:00 AM',
        arrival_time='12:00 PM',
        cost=500
    )
    flight2 = Flight(
        flight_number=456,
        flight_name='Test Flight 2',
        source='Source City 2',
        destination='Destination City 2',
        date='2024-07-11',
        departure_time='11:00 AM',
        arrival_time='1:00 PM',
        cost=600
    )
    db.session.add_all([flight1, flight2])
    db.session.commit()

    booking1 = Booking(user_id=user_id, flight_id=flight1.id)
    booking2 = Booking(user_id=user_id, flight_id=flight2.id)
    db.session.add_all([booking1, booking2])
    db.session.commit()

    # Test retrieving bookings for the logged-in user
    response = test_client.get(f'/bookings?user_id={user_id}')
    assert response.status_code == 200

    bookings_list = response.json
    assert len(bookings_list) == 2  # Adjust based on actual number of bookings expected

    # Check details of each booking
    assert bookings_list[0]['flight_number'] == flight1.flight_number
    assert bookings_list[0]['flight_name'] == 'Test Flight 1'
    assert bookings_list[1]['flight_number'] == flight2.flight_number
    assert bookings_list[1]['flight_name'] == 'Test Flight 2'

    # Clean up: Delete bookings and flights (optional, depending on your application logic)
    db.session.delete(booking1)
    db.session.delete(booking2)
    db.session.delete(flight1)
    db.session.delete(flight2)
    db.session.commit()
