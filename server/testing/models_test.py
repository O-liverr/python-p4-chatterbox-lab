from datetime import datetime
import pytest
from app import app
from models import db, Message

class TestMessage:
    """Tests for the Message model."""

    @pytest.fixture(autouse=True, scope="function")
    def setup_and_teardown(self):
        """Set up database tables before each test, and drop after."""
        with app.app_context():
            db.create_all()
            yield
            db.drop_all()

    def test_has_correct_columns(self):
        """Has columns for message body, username, and creation time."""
        with app.app_context():
            hello_from_liza = Message(body="Hello 👋", username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert isinstance(hello_from_liza.created_at, datetime)

