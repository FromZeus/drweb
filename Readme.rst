|language| |license|

===========
Sample Task
===========

Description
~~~~~~~~~~~

Service for solving difficult issues.

How to use
~~~~~~~~~~

master
^^^^^^

Run: ``docker-compose up -d``.

Application will appear at 5000 port.

feature/openshift
^^^^^^^^^^^^^^^^^
* Quick installing of minishift

  https://docs.openshift.org/latest/minishift/getting-started/installing.html#installing-instructions

* `minishift start --openshift-version=v3.7.0`

  `minishift console`

* `oc login -u developer -p dev`

  `oc new-project sample`

* `eval $(minishift docker-env)`

  `docker login -u developer -p $(oc whoami -t) $(minishift openshift registry)`

  `docker pull rabbitmq:3.6.12-alpine`

  `docker tag rabbitmq:3.6.12-alpine $(minishift openshift registry)/sample/rabbitmq:3.6.12-alpine`

  `docker push $(minishift openshift registry)/sample/rabbitmq:3.6.12-alpine`

* `git co feature/openshift`

  `oc new-app openshift/templates/template-mystack.yml`

* Look at your browser and wait for deployment

* Remove all related to this stack

  `oc delete pods,services,routes,imagestreams,buildconfigs,imageStreamtags,deployments,deploymentconfigs,secrets -l name=mystack`

arguments
^^^^^^^^^

* ``TODO`` - TODO

.. |language| image:: https://img.shields.io/badge/language-python-blue.svg
.. |license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg
