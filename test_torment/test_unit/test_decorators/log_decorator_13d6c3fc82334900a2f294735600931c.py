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

    'expected': [
        'INFO:torment.decorators:STARTING: failure()',
        'ERROR:torment.decorators:EXCEPTION: failure()',
        'INFO:torment.decorators:STOPPING: failure()'
    ],
})
