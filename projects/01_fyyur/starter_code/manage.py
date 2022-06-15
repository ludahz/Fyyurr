import os
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from filters import format_datetime

from flask_migrate import Migrate, MigrateCommand

# from app import app

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
app.jinja_env.filters['datetime'] = format_datetime
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
