FROM python:3.6-alpine3.7

LABEL mantainers="asteroid566@gmail.com"

ENV HOME=/opt/app-root/src \
    PATH=/opt/app-root/src/bin:/opt/app-root/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:$PATH

RUN echo "default:x:1000130000:0::/opt/app-root:" >> /etc/passwd && \
echo "default:!:$(($(date +%s) / 60 / 60 / 24)):0:99999:7:::" >> /etc/shadow && \
echo "default:x:1000130000:" >> /etc/group && \
mkdir mkdir -p ${HOME} && chown -R 1000130000:0 /opt/app-root

#RUN mkdir -p ${HOME} && \
#adduser -s /bin/sh -u 1000130000 -G root -h ${HOME} -S -D default && \
#chown -R 1000130000:0 /opt/app-root

RUN pip install pika flask flask_sqlalchemy \
flask_script flask_migrate flask_wtf wtforms

WORKDIR /opt/app-root/src

EXPOSE 8080
USER 1000130000

ADD ./ /opt/app-root/src

ENTRYPOINT su - 1001 -c "python server.py"
