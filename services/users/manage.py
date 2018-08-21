# manage.py is used to the configure Flask CLI to run
# and manage the app from the command line.

from flask.cli import FlaskGroup
from project import app

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()