# manage.py is used to the configure Flask CLI to run
# and manage the app from the command line.
import unittest
import coverage

from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

# Configure the coverages reports
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()

# Create the users app
app = create_app()
cli = FlaskGroup(create_app=create_app)

# Make the `recreate_db` command accessible from the command line
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Make the `test` command accessible from the command line
@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# Make the `seed_db` command accessible from the command line
@cli.command()
def seed_db():
    """Seeds the database (i.e. adds some initial data)"""
    db.session.add(User(username='josh', email="bolualawode@gmail.com"))
    db.session.add(User(username='jondoe', email="jon@doe.com"))
    db.session.commit()

# Make the `cov` command accessible from the command line
@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()