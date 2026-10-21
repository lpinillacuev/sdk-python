"""Unit tests for the Stores resource using a mock HTTP client."""
import json
import unittest

from mercadopago.resources import Stores
from tests.base_client_test import BaseClientTest


class TestStores(BaseClientTest):
    """Test Module: Stores"""

    def test_create_store(self):
        payload = {"name": "Main store", "external_id": "main-001"}
        self.mock_post({"id": "store-001"}, status=201)

        result = self.sdk.stores().create_store(123, payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_search_stores(self):
        self.mock_get({"results": []})

        result = self.sdk.stores().search_stores(123, {"external_id": "main-001"})

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores/search", kwargs["url"])
        self.assertEqual({"external_id": "main-001"}, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_delete_store(self):
        self.mock_delete({"id": "store-001"})

        result = self.sdk.stores().delete_store(123, "store-001")

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores/store-001", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_update_store(self):
        payload = {"name": "Updated store", "external_id": "updated-001"}
        self.mock_put({"id": "store-001"})

        result = self.sdk.stores().update_store(123, "store-001", payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores/store-001", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_get_store(self):
        self.mock_get({"id": "store-001"})

        resource = self.sdk.stores()
        self.assertIsInstance(resource, Stores)
        result = resource.get_store("store-001")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/stores/store-001", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()