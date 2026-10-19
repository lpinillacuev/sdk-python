"""Tests for retrieving a store through the SDK."""
import unittest

from mercadopago.core import MPBase
from mercadopago.resources.store import Store
from tests.base_client_test import BaseClientTest


class TestStore(BaseClientTest):
    """Store lookup over the SDK's HTTP client."""

    def test_get_store_by_id(self):
        store = {"id": "store-001", "name": "Main Branch"}
        self.mock_get(store)

        resource = self.sdk.store()
        self.assertIsInstance(resource, Store)
        self.assertIsInstance(resource, MPBase)
        result = resource.get("store-001")

        self.assertEqual(200, result["status"])
        self.assertEqual(store, result["response"])
        self.mock_http.get.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/stores/store-001",
            self.mock_http.get.call_args.kwargs["url"],
        )

    def test_create_store(self):
        store = {"id": "store-001", "name": "Main Branch"}
        payload = {
            "name": "Main Branch",
            "external_id": "branch-1",
            "business_hours": {"monday": [{"open": "09:00", "close": "18:00"}]},
            "location": {"street_name": "Main Street", "street_number": "12"},
        }
        self.mock_post(store, status=201)

        result = self.sdk.store().create_store(123, payload)

        self.assertEqual(201, result["status"])
        self.assertEqual(store, result["response"])
        self.mock_http.post.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/users/123/stores",
            self.mock_http.post.call_args.kwargs["url"],
        )
        self.assertEqual(payload, __import__("json").loads(self.mock_http.post.call_args.kwargs["data"]))
        self.assertEqual("application/json", self.mock_http.post.call_args.kwargs["headers"]["Content-type"])

    def test_search_stores(self):
        response = {"paging": {"total": 1, "limit": 30, "offset": 0},
                    "results": [{"id": "store-001", "name": "Main Branch"}]}
        self.mock_get(response)

        result = self.sdk.store().search_stores(123, "branch-1")

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.get.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/users/123/stores/search",
            self.mock_http.get.call_args.kwargs["url"],
        )
        self.assertEqual({"external_id": "branch-1"}, self.mock_http.get.call_args.kwargs["params"])

    def test_delete_store(self):
        self.mock_delete({"id": "store-001"}, status=200)

        result = self.sdk.store().delete_store("12/3", "store/001")

        self.assertEqual(200, result["status"])
        self.mock_http.delete.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/users/12%2F3/stores/store%2F001",
            self.mock_http.delete.call_args.kwargs["url"],
        )

    def test_update_store(self):
        payload = {"name": "New Branch", "external_id": "branch-2",
                   "business_hours": {"monday": [{"open": "10:00", "close": "19:00"}]},
                   "location": {"city_name": "Sao Paulo"}}
        store = {"id": "store-001", **payload}
        self.mock_put(store)

        result = self.sdk.store().update_store(123, "store/001", payload)

        self.assertEqual(200, result["status"])
        self.assertEqual(store, result["response"])
        self.mock_http.put.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/users/123/stores/store%2F001",
            self.mock_http.put.call_args.kwargs["url"],
        )
        self.assertEqual(payload, __import__("json").loads(self.mock_http.put.call_args.kwargs["data"]))
        self.assertEqual("application/json", self.mock_http.put.call_args.kwargs["headers"]["Content-type"])


if __name__ == "__main__":
    unittest.main()