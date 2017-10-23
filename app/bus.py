import pika

from app import db
from .models import Task


class Bus(object):
    @staticmethod
    def send_task_to_db(task):
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def get_task_from_db(id=None, **filter_by):
        if id is not None:
            return Task.query.get(id)
        elif filter_by is not None:
            return Task.query.filter_by(filter_by).first()
        else:
            return None

    @staticmethod
    def update_task_in_db(task, **update):
        t = Bus.get_task_from_db(task.id)
        for k, v in update.iteritems():
            setattr(t, k, v)
        db.session.commit()

    @staticmethod
    def send_task_to_queue(task, host, queue, user, password):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                credentials=pika.PlainCredentials(user, password)
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange="",
                              routing_key=queue,
                              body=str(task.id))
        connection.close()

    @staticmethod
    def get_task_from_queue(host, queue, user, password):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                credentials=pika.PlainCredentials(user, password)
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        id = channel.basic_get(queue=queue, no_ack=True)
        connection.close()

        if id[2] is not None:
            task = Bus.get_task_from_db(int(id[2]))
        else:
            task = None

        return task
