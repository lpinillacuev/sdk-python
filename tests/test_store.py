"""Wire-level tests for the Stores resource."""
import unittest

from tests.base_client_test import BaseClientTest


class TestStore(BaseClientTest):
    """Test Module: Store"""

    def test_get_store(self):
        """The SDK factory retrieves a store by an escaped ID over GET."""
        fixture = {"id": "shop/42", "name": "Test store"}
        self.mock_get(fixture)

        result = self.sdk.store().get_store("shop/42")

        self.assertEqual(200, result["status"])
        self.assertEqual(fixture, result["response"])
        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertIn("/stores/shop%2F42", str(args) + str(kwargs))


if __name__ == "__main__":
    unittest.main()