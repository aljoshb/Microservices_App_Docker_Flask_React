# manage.py is used to the configure Flask CLI to run
# and manage the app from the command line.
import unittest

from flask.cli import FlaskGroup
from project import app, db

cli = FlaskGroup(app)

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

if __name__ == '__main__':
    cli()