#
# Author:: Noah Kantrowitz <noah@coderanger.net>
#
# Copyright 2014, Noah Kantrowitz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import inspect

from fabric.main import find_fabfile, load_fabfile

def unwrap(task):
    """Unwrap a Fabric task to find the original function object."""
    # Unwrap
    while hasattr(task, 'wrapped'):
        task = task.wrapped
    # Smash the closure
    if task.func_code.co_name == 'inner_decorator':
        closure = dict(zip(task.func_code.co_freevars, (c.cell_contents for c in task.func_closure)))
        task = closure.get('func', closure.get('fn', task))
    return task


def visit_task(task, path):
    """Extract all needed information from a task."""
    task = unwrap(task)
    args = inspect.getargspec(task)
    return {
        'name': task.func_name,
        'path': path,
        'doc': task.__doc__,
        'cron': getattr(task, 'rundeck_cron', None),
        'argspec': {
            'args': args.args,
            'varargs': args.varargs,
            'keywords': args.keywords,
            'defaults': args.defaults,
        },
    }


def visit(c, path=()):
    """Recursively process all tasks in a fabfile."""
    ret = []
    for key, value in sorted(c.iteritems()):
        if isinstance(value, dict):
            ret.extend(visit(value, path + (key,)))
        else:
            ret.append(visit_task(value, path))
    return ret


def visit_fabfile(path=None):
    """Load and process a fabfile from the current working directory."""
    path = path or find_fabfile()
    if not path:
        raise ValueError('No fabfile detected')
    callables = load_fabfile(path)[1]
    return visit(callables)
