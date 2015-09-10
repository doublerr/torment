# Copyright 2015 Alex Brandt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from torment import fixtures

from test_torment.test_unit.test_decorators import LogDecoratorFixture


def failure():
    raise RuntimeError()

fixtures.register(globals(), ( LogDecoratorFixture, ), {
    'function': failure,

    'parameters': {
        'prefix': 'prefix',
    },

    'expected': [
        'INFO:torment.decorators:STARTING: prefixfailure()',
        'ERROR:torment.decorators:EXCEPTION: prefixfailure()\n'
        'Traceback (most recent call last):\n'
        '  File "/home/alunduil/Projects/kumoru/torment/torment/decorators.py", '
        'line 65, in wrapper\n'
        '    return function(*args, **kwargs)\n'
        '  File '
        '"/home/alunduil/Projects/kumoru/torment/test_torment/test_unit/test_decorators/log_decorator_af21ed4f310b4148a29697cb1383622f.py", '
        'line 21, in failure\n'
        '    raise RuntimeError()\n'
        'RuntimeError',
        'INFO:torment.decorators:STOPPING: prefixfailure()',
    ]
})
