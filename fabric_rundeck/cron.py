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

from .visitor import unwrap

def cron(spec=None, **kwargs):
    """Decorator to mark a task as being on a cron schedule."""
    if not (spec or kwargs):
        raise ValueError('You must pass either a cron spec or keyword arguments')
    def decorator(fn):
        original = unwrap(fn)
        original.rundeck_cron = spec or kwargs
        return fn
    return decorator


def hourly(fn):
    return cron('0 * * * *')(fn)


def daily(fn):
    return cron('0 0 * * *')(fn)


def monthly(fn):
    return cron('0 0 0 * *')(fn)
