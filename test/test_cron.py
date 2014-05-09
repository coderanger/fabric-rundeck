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

from fabric.api import task, roles
import pytest

from fabric_rundeck import cron, hourly, daily, monthly, visitor


@pytest.fixture
def fn():
    def fn():
        pass
    return fn


class TestCron(object):
    def test_cron_task(self, fn):
        t = cron('* * * * *')(task(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == '* * * * *'

    def test_task_cron(self, fn):
        t = task(cron('* * * * *')(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == '* * * * *'

    def test_cron_task_hash(self, fn):
        t = cron(time={'minute': '*'})(task(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == {'time': {'minute': '*'}}

    def test_task_cron_hash(self, fn):
        t = task(cron(time={'minute': '*'})(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == {'time': {'minute': '*'}}


class TestHourly(object):
    def test_simple(self, fn):
        t = hourly(task(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == '0 * * * *'


class TestDaily(object):
    def test_simple(self, fn):
        t = daily(task(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == '0 0 * * *'


class TestMonthly(object):
    def test_simple(self, fn):
        t = monthly(task(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == '0 0 0 * *'
