FROM python:3.6-alpine3.7

LABEL mantainers="asteroid566@gmail.com"

ENV HOME=/opt/app-root/src \
    PATH=/opt/app-root/src/bin:/opt/app-root/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:$PATH

RUN mkdir -p ${HOME} && \
adduser -s /bin/sh -u 1000070000 -G root -h ${HOME} -S -D default && \
chown -R 1001:0 /opt/app-root

RUN pip install pika flask flask_sqlalchemy \
flask_script flask_migrate flask_wtf wtforms

WORKDIR /opt/app-root/src

EXPOSE 8080
USER 1001

ADD ./ /opt/app-root/src

ENTRYPOINT python server.py
