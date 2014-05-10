fabric_rundeck
==============

Provides helpers for integration between Fabric_ and Rundeck_, via
rundeck-fabric_.

.. _Fabric: http://fabfile.org/
.. _Rundeck: http://rundeck.org/
.. _rundeck-fabric: https://github.com/balanced-cookbooks/rundeck-fabric

Cron
----

You can add scheduled execution to a fabric task using the ``cron`` helper::

    from fabric.api import task
    from fabric_rundeck import cron

    @cron('0 12 * * *')
    @task
    def mytask():
        pass


There are also helpers for ``hourly``, ``daily``, and ``monthly``::

    from fabric.api import task
    from fabric_rundeck import daily

    @daily
    @task
    def mytask():
        pass

