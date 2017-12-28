import pika

from app import db
from .models import Task


class Bus(object):

    class DataBase(object):
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
        def update_task_in_db(id, **update):
            t = Bus.DataBase.get_task_from_db(id)
            for k, v in update.items():
                setattr(t, k, v)
            db.session.commit()

    class Queue(object):
        def __init__(self, host, user, password, routing_key):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    credentials=pika.PlainCredentials(user, password),
                    heartbeat_interval=0
                )
            )
            self.routing_key = routing_key

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.remove()

        def remove(self):
            self.connection.close()

        def send_task_to_queue(self, task, queue):
            channel = self.connection.channel()
            channel.exchange_declare(exchange="ex",
                                     exchange_type="topic")
            channel.queue_declare(queue=queue)
            channel.basic_publish(exchange="ex",
                                  routing_key=self.routing_key,
                                  body=str(task.id))

        def get_task_from_queue(self, queue):
            channel = self.connection.channel()
            channel.exchange_declare(exchange="ex",
                                     exchange_type="topic")
            channel.queue_declare(queue=queue)
            id = channel.basic_get(queue=queue, no_ack=True)

            if id[2] is not None:
                task = Bus.DataBase.get_task_from_db(int(id[2]))
            else:
                task = None

            return task

        def consume_tasks(self, queue, callback):
            channel = self.connection.channel()
            channel.exchange_declare(exchange="ex",
                                     exchange_type="topic")
            result = channel.queue_declare(queue=queue)
            channel.queue_bind(result.method.queue,
                               exchange="ex",
                               routing_key=self.routing_key)
            channel.basic_consume(callback,
                                  result.method.queue,
                                  no_ack=True)
            channel.start_consuming()
