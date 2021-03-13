from pladmed.routes import superuser
from flask.cli import with_appcontext
import click
from flask import current_app

@superuser.cli.command('create')
@with_appcontext
@click.argument('email')
@click.argument('password')
def create(email, password):
    print("Creating superuser:", email, "with password:", password)

    current_app.db.users.create_user(
        email=email,
        password=password,
        is_superuser=True,
        credits_=0
    )
