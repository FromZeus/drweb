import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = "top-secret"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = True

HOST = "localhost"
QUEUE = "drweb"
USER = "drweb"
PASSWORD = "password"

MAXIMUM_PARALLEL = 2
RESOLVER_TIMEOUT = 1
