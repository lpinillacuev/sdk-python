"""Unit tests for the Stores resource using a mock HTTP client."""
import json
import unittest

from mercadopago.resources import Stores
from tests.base_client_test import BaseClientTest


class TestStores(BaseClientTest):
    """Test Module: Stores"""

    def test_get_store(self):
        self.mock_get({"id": "store-1"})

        resource = self.sdk.stores()
        self.assertIsInstance(resource, Stores)
        result = resource.get_store("store/1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/stores/store%2F1", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_store(self):
        store_object = {"name": "Main Store", "external_id": "branch-1"}
        self.mock_post({"id": "store-1"}, status=201)

        result = self.sdk.stores().create_store(123, store_object)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/users/123/stores", kwargs["url"])
        self.assertEqual(store_object, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_search_stores(self):
        self.mock_get({"results": []})

        result = self.sdk.stores().search_stores(123, external_id="branch-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/users/123/stores/search", kwargs["url"])
        self.assertEqual({"external_id": "branch-1"}, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_delete_store(self):
        self.mock_delete({}, status=200)

        result = self.sdk.stores().delete_store(123, "store/1")

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual("https://api.mercadopago.com/users/123/stores/store%2F1", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_update_store(self):
        store_object = {"name": "Updated Store", "external_id": "branch-1"}
        self.mock_put({"id": "store-1"})

        result = self.sdk.stores().update_store(123, "store/1", store_object)

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual("https://api.mercadopago.com/users/123/stores/store%2F1", kwargs["url"])
        self.assertEqual(store_object, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()