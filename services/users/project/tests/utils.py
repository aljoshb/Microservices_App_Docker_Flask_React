from project import db
from project.api.models import User


def add_user(username, email):
    """
    Helper function to add users to the database for testing purposes.
    """
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
