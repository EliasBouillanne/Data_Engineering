from flask import Flask
from .views import app

from . import database

@app.cli.command()
def init_db():
    database.init_db()
