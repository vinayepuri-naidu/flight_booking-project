import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Program1 import app, db, User, Flight , Booking # Adjust the import according to your file structure

@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Configure the app for testing
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()  # Create tables
            yield testing_client  # this is where the testing happens!

    # Tear down
    with flask_app.app_context():
        db.drop_all()  # Clean up after tests
