import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
import click
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from .models import db, User, Post

class Base(DeclarativeBase):
    pass


@click.command('init-db')
def init_db_command():
    with current_app.app_context():
        from . import models 
        models.db.create_all()
        click.echo('Banco de dados inicializado com sucesso (Tabelas: User, Post).')
    

import os

def create_app(test_config=None):
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(BASE_DIR, 'teste_.sqlite'),
    ) 

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # inicializa o db PRIMEIRO
    db.init_app(app)

    #  importa models (registra tabelas)
    from . import models

    # registra comando DEPOIS
    app.cli.add_command(init_db_command)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from .controllers.user import app as user_app
    app.register_blueprint(user_app)

    return app