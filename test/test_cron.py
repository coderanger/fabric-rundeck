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

from fabric_rundeck import cron, visitor


class TestCron(object):
    @pytest.fixture
    def fn(self):
        def fn():
            pass
        return fn

    def test_cron_task(self, fn):
        t = cron('* * * * *')(task(fn))
        data = visitor.visit_task(t, ())
        assert data['cron'] == '* * * * *'
