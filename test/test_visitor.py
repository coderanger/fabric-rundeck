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

import os

from fabric.api import task, roles
import pytest

from fabric_rundeck import visitor


def fixture_path(*path):
    return os.path.join(os.path.dirname(__file__), 'data', *path)


class TestUnwrap(object):
    @pytest.fixture
    def fn(self):
        def fn():
            pass
        return fn

    def test_fn(self, fn):
        assert visitor.unwrap(fn) is fn

    def test_task(self, fn):
        t = task(fn)
        assert visitor.unwrap(t) is fn

    def test_taskcall(self, fn):
        t = task()(fn)
        assert visitor.unwrap(t) is fn

    def test_task_roles(self, fn):
        t = task(roles('foo')(fn))
        assert visitor.unwrap(t) is fn

    def test_taskcall_roles(self, fn):
        t = task()(roles('foo')(fn))
        assert visitor.unwrap(t) is fn

    def test_roles_task(self, fn):
        t = roles('foo')(task(fn))
        assert visitor.unwrap(t) is fn

    def test_roles_taskcall(self, fn):
        t = roles('foo')(task()(fn))
        assert visitor.unwrap(t) is fn

    def test_lambda(self):
        fn = lambda: None
        assert visitor.unwrap(fn) is fn

    def test_lambda_task(self):
        fn = lambda: None
        t = task(fn)
        assert visitor.unwrap(t) is fn


class TestVisitTask(object):
    def test_no_args(self):
        def fn():
            pass
        assert visitor.visit_task(fn, ()) == {
            'name': 'fn',
            'path': (),
            'doc': None,
            'cron': None,
            'argspec': {
                'args': [],
                'varargs': None,
                'keywords': None,
                'defaults': None,
            },
        }

    def test_simple_args(self):
        def fn(a, b):
            pass
        assert visitor.visit_task(fn, ()) == {
            'name': 'fn',
            'path': (),
            'doc': None,
            'cron': None,
            'argspec': {
                'args': ['a', 'b'],
                'varargs': None,
                'keywords': None,
                'defaults': None,
            },
        }

    def test_arg_defaults(self):
        def fn(a, b=1, c=None):
            pass
        assert visitor.visit_task(fn, ()) == {
            'name': 'fn',
            'path': (),
            'doc': None,
            'cron': None,
            'argspec': {
                'args': ['a', 'b', 'c'],
                'varargs': None,
                'keywords': None,
                'defaults': (1, None),
            },
        }

    def test_varargs(self):
        def fn(*args, **kwargs):
            pass
        assert visitor.visit_task(fn, ()) == {
            'name': 'fn',
            'path': (),
            'doc': None,
            'cron': None,
            'argspec': {
                'args': [],
                'varargs': 'args',
                'keywords': 'kwargs',
                'defaults': None,
            },
        }

    def test_docs(self):
        def fn(*args, **kwargs):
            """I am a teapot."""
            pass
        assert visitor.visit_task(fn, ()) == {
            'name': 'fn',
            'path': (),
            'doc': 'I am a teapot.',
            'cron': None,
            'argspec': {
                'args': [],
                'varargs': 'args',
                'keywords': 'kwargs',
                'defaults': None,
            },
        }


class TestVisit(object):
    def test_single(self):
        def fn():
            pass
        callables = {
            'fn': fn,
        }
        data = visitor.visit(callables)
        assert len(data) == 1
        assert data[0]['name'] == 'fn'

    def test_multi(self):
        def fn():
            pass
        def fn2():
            pass
        def fn3():
            pass
        callables = {
            'fn': fn,
            'fn2': fn2,
            'fn3': fn3,
        }
        data = visitor.visit(callables)
        assert len(data) == 3
        assert data[0]['name'] == 'fn'
        assert data[1]['name'] == 'fn2'
        assert data[2]['name'] == 'fn3'

    def test_nested(self):
        def fn():
            pass
        def fn2():
            pass
        def fn3():
            pass
        callables = {
            'fn': fn,
            'mod': {
                'fn2': fn2,
                'fn3': fn3,
            }
        }
        data = visitor.visit(callables)
        assert len(data) == 3
        assert data[0]['name'] == 'fn'
        assert data[0]['path'] == ()
        assert data[1]['name'] == 'fn2'
        assert data[1]['path'] == ('mod',)
        assert data[2]['name'] == 'fn3'
        assert data[2]['path'] == ('mod',)


class TestVisitFabfile(object):
    def test_one(self):
        data = visitor.visit_fabfile(fixture_path('fabfile_one.py'))
        assert len(data) == 3
