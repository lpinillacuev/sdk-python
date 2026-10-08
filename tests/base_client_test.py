"""Base class for mock-based unit tests of MercadoPago SDK resources."""
import json
import os
import unittest
from unittest.mock import MagicMock

import mercadopago
from mercadopago.http.http_client import HttpClient


def _load_fixture(filename):
    """Load a JSON fixture from tests/resources/mocks/."""
    base = os.path.dirname(__file__)
    path = os.path.join(base, "resources", "mocks", filename)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class BaseClientTest(unittest.TestCase):
    """Provides a mock HTTP client and an SDK instance for unit tests.

    Sub-classes should call ``self.mock_get``, ``self.mock_post``,
    ``self.mock_put``, or ``self.mock_delete`` to set up the expected
    response *before* calling the resource method under test.
    """

    def setUp(self):
        self.mock_http = MagicMock(spec=HttpClient)
        self.sdk = mercadopago.SDK("TEST_TOKEN", http_client=self.mock_http)

    # ------------------------------------------------------------------
    # Helpers – configure the mock for a single HTTP verb
    # ------------------------------------------------------------------

    def mock_get(self, response_dict, status=200):
        """Make the next ``http_client.get(...)`` return *response_dict*."""
        self.mock_http.get.return_value = {"status": status, "response": response_dict}

    def mock_get_bytes(self, content, status=200):
        """Make the next ``http_client.get(...)`` return raw response bytes."""
        self.mock_http.get.return_value = {"status": status, "response": content}

    def mock_post(self, response_dict, status=201):
        """Make the next ``http_client.post(...)`` return *response_dict*."""
        self.mock_http.post.return_value = {"status": status, "response": response_dict}

    def mock_post_bytes(self, content, status=201):
        """Make the next ``http_client.post(...)`` return raw response bytes."""
        self.mock_http.post.return_value = {"status": status, "response": content}

    def mock_post_multipart(self, response_dict, status=201):
        """Make the next multipart ``http_client.post(...)`` return a response."""
        self.mock_http.post.return_value = {"status": status, "response": response_dict}

    def mock_put(self, response_dict, status=200):
        """Make the next ``http_client.put(...)`` return *response_dict*."""
        self.mock_http.put.return_value = {"status": status, "response": response_dict}

    def mock_patch(self, response_dict, status=200):
        """Make the next ``http_client.patch(...)`` return *response_dict*."""
        self.mock_http.patch.return_value = {"status": status, "response": response_dict}

    def mock_delete(self, response_dict=None, status=204):
        """Make the next ``http_client.delete(...)`` return *response_dict*."""
        self.mock_http.delete.return_value = {"status": status, "response": response_dict}

    def assert_http_call(self, verb, path, data=None, params=None):
        """Assert the common wire arguments for one resource request."""
        expected = {
            "url": "https://api.mercadopago.com" + path,
            "headers": unittest.mock.ANY,
            "timeout": 60.0,
            "maxretries": 3,
            "retry_on": None,
        }
        if verb in ("post", "put"):
            expected["data"] = data
        if verb in ("get", "post", "put", "delete"):
            expected["params"] = params
        getattr(self.mock_http, verb).assert_called_once_with(**expected)

    # ------------------------------------------------------------------
    # Fixture loader exposed to sub-classes
    # ------------------------------------------------------------------

    @staticmethod
    def load_fixture(filename):
        """Return the parsed JSON fixture *filename* from resources/mocks/."""
        return _load_fixture(filename)
