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

import logging
import tornado
import typing  # noqa (use mypy typing)
import unittest

from torment import contexts

logger = logging.getLogger(__name__)

@unittest.skipUnless('tornado' in contexts.tornado.LOADED, 'requires tornado')
class TornadoHttpClientContextPropertyUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.c = contexts.tornado.TornadoHttpClientContext()

    def test_tornadohttpclientcontext_mocks(self) -> None:
        '''torment.contexts.TornadoHttpClientContext.mocks == {'tornado.httpclient'}'''

        self.assertEqual(self.c.mocks, set([ 'tornado.httpclient', ]))


@unittest.skipUnless('tornado' in contexts.tornado.LOADED, 'requires tornado')
class TornadoHttpClientContextMockTornadoHttpclientUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.c = contexts.tornado.TornadoHttpClientContext()

    def test_torandohttpclientcontext_mock_tornado_httpclient(self) -> None:
        '''torment.contexts.TornadoHttpClientContext().mock_tornado_httpclient()'''

        logger.debug('contexts.TestContext: %s', contexts.TestContext)
        logger.debug('self.__module__: %s', self.__module__)

        _ = unittest.mock.patch.object(contexts.TestContext, 'module', self.__module__)
        _.start()
        self.addCleanup(_.stop)

        c = contexts.TestContext()

        c.patch('tornado.httpclient')

        self.assertTrue(hasattr(c, 'mocked_tornado_httpclient'))
        self.assertIsInstance(c.mocked_tornado_httpclient, unittest.mock.MagicMock)
        self.assertIsInstance(c.mocked_tornado_httpclient.AsyncHTTPClient, unittest.mock.MagicMock)
        self.assertIsInstance(c.mocked_tornado_httpclient.HTTPClient, unittest.mock.MagicMock)
        self.assertIsInstance(c.mocked_tornado_httpclient.HTTPError, type(tornado.httpclient.HTTPError))
