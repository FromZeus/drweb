FROM python:3.5-alpine

LABEL mantainers="asteroid566@gmail.com"

RUN pip install pika flask flask_sqlalchemy \
flask_script flask_migrate flask_wtf wtforms

WORKDIR /opt/drweb

EXPOSE 8080

ADD ./ /opt/drweb

#ENTRYPOINT python server.py