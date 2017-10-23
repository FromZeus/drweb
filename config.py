import os


# Flask
WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED", True)
SECRET_KEY = os.environ.get("SECRET_KEY", "top-secret")

# SQLAlchemy
basedir = os.environ.get("SQLALCHEMY_DATABASE_BASE",
    os.path.abspath(os.path.dirname(__file__)))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "migrations")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS", True)

# RabbitMQ
HOST = os.environ.get("RABBIT_HOST", "rabbit")
QUEUE = os.environ.get("RABBIT_QUEUE", "drweb")
USER = os.environ.get("RABBIT_USER", "drweb")
PASSWORD = os.environ.get("RABBIT_PASSWORD", "password")

# Resolver
RESOLVER_MAXIMUM_PARALLEL = os.environ.get("MAXIMUM_PARALLEL", 2)
RESOLVER_TIMEOUT = os.environ.get("RESOLVER_TIMEOUT", 1)
RESOLVER_LOGFILE = os.environ.get("RESOLVER_LOGFILE", None)
RESOLVER_LOGLEVEL = os.environ.get("RESOLVER_LOGLEVEL", "INFO")

APP_PORT = os.environ.get("APP_PORT", 8080)
