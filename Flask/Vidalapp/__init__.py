from flask import Flask
from .views import app

from . import utils

@app.cli.command('initdb')
def init_db():
    utils.init_db()
