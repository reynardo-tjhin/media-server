import sqlite3
import click

from datetime import datetime
from flask import Flask, current_app, g

def get_db():
    if 'db' not in g:
        # g is a special object that is unique for each request
        # it is used to store data that might be accessed by multiple functions
        # during the request.
        # The connection is stored and reused insted of creating a new connection
        # if `get_db` is called a second time in the same request.
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    `close_db` checks if a connection was created by checking if `g.db` was set.
    If the connection exists, it is closed.
    """
    db = g.pop('db', None)

    if (db is not None):
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo("Initialized the database.")

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
