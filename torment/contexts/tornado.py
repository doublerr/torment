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
import typing  # noqa (use mypy typing)

LOADED = set()
try:
    import tornado.httpclient
    LOADED.add('tornado')
except ImportError:
    pass

from torment import contexts
from torment import decorators

logger = logging.getLogger(__name__)


class TornadoHttpClientContext(contexts.TestContext):
    '''Provide tornado.httpclient context for testing fixtures.

    Extends ``torment.contexts.TestContext``.

    **Public Methods**

    * ``mock_tornado_httpclient``

    **Class Variables**

    :``mocks``: cf. `torment.contexts.TestContext`

    '''

    mocks = set()

    mocks.add('tornado.httpclient')

    @decorators.mock('tornado.httpclient')
    def mock_tornado_httpclient(self) -> None:
        '''Mocks tornado.httpclient.

        **Patches**

        * ``tornado.httpclient`` within the actual module

        **Created Properties**

        Mocks:

        * ``mocked_tornado_httpclient``
        * ``mocked_tornado_httpclient.AsyncHTTPClient``
        * ``mocked_tornado_httpclient.HTTPClient``
        * ``mocked_tornado_httpclient.HTTPError``

        '''

        if 'tornado' not in LOADED:
            logger.warn('tornado not available–not mocking tornado.httpclient')
            return

        originals = {
            'HTTPError': tornado.httpclient.HTTPError,
        }

        self.patch('tornado.httpclient')

        self.mocked_tornado_httpclient_asynchttpclient = unittest.mock.MagicMock()
        self.mocked_tornado_httpclient.AsyncHTTPClient.return_value = self.mocked_tornado_httpclient_asynchttpclient

        self.mocked_tornado_httpclient_httpclient = unittest.mock.MagicMock()
        self.mocked_tornado_httpclient.HTTPClient.return_value = self.mocked_tornado_httpclient_httpclient

        type(self.mocked_tornado_httpclient).HTTPError = originals['HTTPError']
