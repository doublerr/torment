# Copyright 2015 Alex Brandt <alex.brandt@rackspace.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tornado.concurrent
import unittest.mock

from torment import fixtures


class TornadoHttpClientFixture(fixtures.Fixture):
    def initialize(self):
        super().initialize()

        future = tornado.concurrent.Future()
        future._done = True  # Future's aren't done even when a set_ is called.

        if 'fetch' in self.expected:
            if 'future' in self.expected['fetch']:
                if 'result' in self.expected['fetch']['future']:
                    future.set_result(unittest.mock.PropertyMock(**self.expected['fetch']['future']['result']))

                if 'exception' in self.expected['fetch']['future']:
                    future.set_exception(self.expected['fetch']['future']['exception'])

                self.expected['fetch']['future'] = future
            else:
                if 'result' in self.expected['fetch']:
                    self.expected['fetch'] = unittest.mock.PropertyMock(**self.expected['fetch']['result'])

    def setup(self):
        super().setup()

        if self.context.mock_tornado_httpclient():
            self.context.mocked_tornado_httpclient_asynchttpclient.fetch.return_value = self.expected['fetch']['future']

    def check(self):
        super().check()

        if 'result' in self.expected:
            self.context.assertEqual(self.expected['result'], self.result)
