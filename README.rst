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

Fabfile Information
-------------------

Run this module (``python -m fabric_rundeck``) to print information about the
local fabfile to stdout in JSON format::

    $ python -m fabric_rundeck
    [
      {
        "cron": null,
        "path": [],
        "argspec": {
          "keywords": null,
          "args": [],
          "defaults": null,
          "varargs": null
        },
        "name": "mytask",
        "doc": null
      }
    ]

You can also pass a path to a fabfile explicitly::

    $ python -m fabric_rundeck path/to/fabfile.py
    ...
