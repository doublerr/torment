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
    '''Standard fixture for testing Tornado's httpclients

    This fixture can be used to test your code integrations with both 
    ``tornado.httpclient.AsyncHTTPClient`` and 
    ``tornado.httpclient.HTTPClient``. You may also use this fixture to test 
    ``tornado.httpclient.HTTPError``.  Futures for
    ``tornado.httpclient.AsyncHTTPClient`` responses, will automatically be resolved.

    In general, you'll need to populate the response you're expecting from
    a ``tornado.httpclient.AsyncHTTPClient()`` call(). See Examples for more details.
    
    .. note::
       1. This fixture is expected to be used with the ``torment.contexts.test_tornado`` context.
       2. ``self.expected`` is the expected result (return) of your function.

    **Examples**

    Standard AsyncHTTPClient Fixture Class:

    .. code-block:: python

       class MyHTTPClientFixture(TornadoHttpClientFixture):
           @property
           def description(self):
               return super().description + '.my_http_client_function()'

           def run(self):
               self.result = self.context.io_loop.run_sync(functools.partial(my_http_client_fuction))


    Unit Test with Context:

    .. code-block:: python

        class MyHTTPClientUnitTest(TornadoContext):
            fixture_classes = (
                MyHTTPClientFixture,
            )

    Data to be used for test:

    .. code-block:: python

        fixtures.register(globals(), ( MyHTTPClientFixture, ), {
            'mocks': {
                'tornado.httpclient.AsyncHTTPClient.fetch': {
                    'future': {
                        'result': {
                            'body': 'foo',
                            'code': 200,
                            'error': None,
                        },
                    },
                },
            },

            'expected': 'my result'
        })

    '''

    def initialize(self):
        '''Set the expected HTTPClient response as properties on mock
        
        Convert keys within ``self.mocks['tornado.httpclient']['AsyncHTTPClient']['fetch']``
        to properties on ``mocked_tornado_httpclient_asynchttpclient.fetch``.

        '''
    
        super().initialize()

        future = tornado.concurrent.Future()
        future._done = True  # Future's aren't done even when a set_ is called.

        fetch = 'tornado.httpclient.AsyncHTTPClient.fetch'
        fetch = self.mocks.

        if 'fetch' in self.mocks:
            if 'future' in self.mocks[fetch]:  # AsyncHTTPClient
                if 'result' in self.mocks[fetch]['future']:
                    future.set_result(unittest.mock.PropertyMock(**self.mocks[fetch]['future']['result']))

                if 'exception' in self.mocks[fetch]['future']:
                    future.set_exception(self.mocks[fetch]['future']['exception'])

                self.mocks[fetch]['future'] = future
            else:                              # HTTPClient
                if 'result' in self.mocks[fetch]:
                    self.mocks[fetch] = unittest.mock.PropertyMock(**self.mocks[fetch]['result'])

    def setup(self):
        super().setup()

        if self.context.mock_tornado_httpclient():
            self.context.mocked_tornado_httpclient_asynchttpclient.fetch.return_value = self.mocks[fetch]['future']

    def check(self):
        '''Check that the expected output matches the actual result
            
        .. note::
           1. Your ``run()`` function must set it's result to ``self.result``.
           2. set ``self.expected`` to None if there is no return value.

        '''

        super().check()

        self.context.assertEqual(self.expected, self.result)
