#!/usr/bin/env python3
import pytest
from app import app, db
from models import Message

# Keep your custom test name formatting
def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


# ⚡ Add this part for database setup
@pytest.fixture(scope='function')
def test_app():
    """Test app with in-memory database and seeded message."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        # ✅ Seed an example message
        message = Message(body="Hello 👋", username="Liza")
        db.session.add(message)
        db.session.commit()
        yield app
        db.drop_all()
