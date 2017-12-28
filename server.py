#!/usr/bin/python

from app import app


from config import HOST, QUEUE, USER, PASSWORD, ROUTING_KEY
Q = Bus.Queue(HOST, USER, PASSWORD, ROUTING_KEY)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["APP_PORT"], debug=True)
