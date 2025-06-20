import pytest
from datetime import datetime
from app import app
from models import db, Message

@pytest.fixture(autouse=True, scope="function")
def setup_and_teardown():
    """Create tables, clean test messages before each test, and drop tables after."""
    with app.app_context():
        db.create_all()
        m = Message.query.filter_by(body="Hello 👋", username="Liza").all()
        for message in m:
            db.session.delete(message)
        db.session.commit()
    yield
    # Optional: Drop tables after test
    with app.app_context():
        db.drop_all()


class TestApp:
    """Flask application in app.py"""

    def test_has_correct_columns(self):
        """Check the Message model has the right columns."""
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert isinstance(hello_from_liza.created_at, datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_the_database(self):
        """returns a list of JSON objects for all messages in the database."""
        with app.app_context():
            response = app.test_client().get("/messages")
            records = Message.query.all()

            for message in response.json:
                assert message["id"] in [record.id for record in records]
                assert message["body"] in [record.body for record in records]

    def test_creates_new_message_in_the_database(self):
        """creates a new message in the database."""
        with app.app_context():
            app.test_client().post(
                "/messages",
                json={"body": "Hello 👋", "username": "Liza"}
            )
            h = Message.query.filter_by(body="Hello 👋").first()
            assert h is not None
            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        """returns data for the newly created message as JSON."""
        with app.app_context():
            response = app.test_client().post(
                "/messages",
                json={"body": "Hello 👋", "username": "Liza"}
            )
            assert response.content_type == "application/json"
            assert response.json["body"] == "Hello 👋"
            assert response.json["username"] == "Liza"

            h = Message.query.filter_by(body="Hello 👋").first()
            assert h is not None
            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        """updates the body of a message in the database."""
        with app.app_context():
            # Create a message
            m = Message(body="Original 👋", username="Liza")
            db.session.add(m)
            db.session.commit()
            id = m.id

            # Update the message
            app.test_client().patch(
                f"/messages/{id}",
                json={"body": "Goodbye 👋"}
            )
            g = Message.query.filter_by(body="Goodbye 👋").first()
            assert g is not None
            db.session.delete(g)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        """returns data for the updated message as JSON."""
        with app.app_context():
            m = Message(body="Original 👋", username="Liza")
            db.session.add(m)
            db.session.commit()
            id = m.id

            response = app.test_client().patch(
                f"/messages/{id}",
                json={"body": "Goodbye 👋"}
            )
            assert response.content_type == "application/json"
            assert response.json["body"] == "Goodbye 👋"

            g = Message.query.filter_by(body="Goodbye 👋").first()
            db.session.delete(g)
            db.session.commit()

    def test_deletes_message_from_database(self):
        """deletes the message from the database."""
        with app.app_context():
            hello_from_liza = Message(body="Hello 👋", username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(f"/messages/{hello_from_liza.id}")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert h is None
