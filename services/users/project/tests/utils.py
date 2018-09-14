from project import db
from project.api.models import User


def add_user(username, email, password):
    """
    Helper function to add users to the database for testing purposes.
    """
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_admin(username, email, password):
    """
    Helper function to add an admin user to the database for testing purposes.
    """
    user = User(
        username=username,
        email=email,
        password=password)
    user.admin = True
    db.session.add(user)
    db.session.commit()
    return user
