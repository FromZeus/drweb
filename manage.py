from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db
from app.models import Task


app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
