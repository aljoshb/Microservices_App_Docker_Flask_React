# manage.py is used to the configure Flask CLI to run
# and manage the app from the command line.

from flask.cli import FlaskGroup
from project import app, db

cli = FlaskGroup(app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    cli()