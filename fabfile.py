from fabric.api import task, local
from fabric.decorators import roles
from fabric_rundeck import cron

@cron('foo')
@roles('www')
@task
def one():
    """Task one."""
    local('echo one')


@task
def two(arg1):
    """Task
    two."""
    local('echo two %s'%(arg1,))

@task
@roles('www')
def three(c, d=1):
    """Take three."""
    local('echo three %s %s'%(c, d))
