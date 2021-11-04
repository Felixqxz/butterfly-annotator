import click
from flask.cli import with_appcontext

from .database.access import db


@click.command('create_all', help="Create all tables in the app's databases")
@with_appcontext
def create_all():
    db.create_all()


@click.command('drop_all', help='Drop all tables in the specified database')
@with_appcontext
def drop_all():
    db.drop_all()
