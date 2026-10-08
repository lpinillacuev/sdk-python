"""Unit tests for Store and POS operations on the User resource."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestUser(BaseClientTest):
    """Test Module: User"""

    def test_get(self):
        fixture = self.load_fixture("user_get.json")
        self.mock_get(fixture)
        result = self.sdk.user().get()
        self.assertEqual(200, result["status"])
        self.assertEqual(12345, result["response"]["id"])
        self.assertEqual("test@example.com", result["response"]["email"])
        self.mock_http.get.assert_called_once()

    def test_store_operations(self):
        store = {
            "name": "Main Branch",
            "external_id": "STORE-1",
            "business_hours": {"monday": [{"open": "09:00", "close": "18:00"}]},
            "location": {
                "street_number": "100",
                "street_name": "Main Street",
                "city_name": "Sao Paulo",
                "state_name": "SP",
                "zip_code": "01310-100",
                "latitude": -23.56,
                "longitude": -46.65,
            },
        }

        self.mock_post({"id": "1"}, status=201)
        self.sdk.user().create_store(123, store)
        post = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/users/123/stores", post["url"])
        self.assertEqual(store, json.loads(post["data"]))

        self.mock_get({"id": "1"})
        self.sdk.user().get_store("store/id")
        self.assertEqual(
            "https://api.mercadopago.com/stores/store%2Fid",
            self.mock_http.get.call_args.kwargs["url"],
        )

        filters = {"external_id": "STORE-1"}
        self.mock_get({"results": []})
        self.sdk.user().search_stores(123, filters)
        search = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/users/123/stores/search", search["url"]
        )
        self.assertEqual(filters, search["params"])

        self.mock_put({"id": "1"})
        self.sdk.user().update_store(123, "1", store)
        put = self.mock_http.put.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/users/123/stores/1", put["url"])
        self.assertEqual(store, json.loads(put["data"]))

        self.mock_delete({})
        self.sdk.user().delete_store(123, "1")
        self.assertEqual(
            "https://api.mercadopago.com/users/123/stores/1",
            self.mock_http.delete.call_args.kwargs["url"],
        )

    def test_pos_operations(self):
        pos = {
            "name": "Main POS",
            "store_id": "1",
            "external_id": "POS-1",
            "external_store_id": "STORE-1",
            "category": 621102,
            "fixed_amount": False,
            "url": "https://example.com/pos",
        }

        self.mock_post({"id": "2"}, status=201)
        self.sdk.user().create_pos(pos)
        post = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/pos", post["url"])
        self.assertEqual(pos, json.loads(post["data"]))

        self.mock_get({"id": "2"})
        self.sdk.user().get_pos("pos/id")
        self.assertEqual(
            "https://api.mercadopago.com/pos/pos%2Fid",
            self.mock_http.get.call_args.kwargs["url"],
        )

        filters = {
            "external_id": "POS-1",
            "external_store_id": "STORE-1",
            "store_id": "1",
            "category": 621102,
        }
        self.mock_get({"results": []})
        self.sdk.user().search_pos(filters)
        search = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/pos", search["url"])
        self.assertEqual(filters, search["params"])

        self.mock_put({"id": "2"})
        self.sdk.user().update_pos("2", pos)
        put = self.mock_http.put.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/pos/2", put["url"])
        self.assertEqual(pos, json.loads(put["data"]))

        self.mock_delete({})
        self.sdk.user().delete_pos("2")
        self.assertEqual(
            "https://api.mercadopago.com/pos/2",
            self.mock_http.delete.call_args.kwargs["url"],
        )

        self.mock_get([])
        self.sdk.user().list_pos(123)
        self.assertEqual(
            "https://api.mercadopago.com/users/123/pos",
            self.mock_http.get.call_args.kwargs["url"],
        )

    def test_store_and_pos_bodies_require_dictionaries(self):
        with self.assertRaises(ValueError):
            self.sdk.user().create_store(123, "not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.user().update_store(123, "1", "not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.user().create_pos("not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.user().update_pos("1", "not-a-dict")

    def test_tag_oriented_factories_preserve_user_compatibility(self):
        user_type = type(self.sdk.user())
        self.assertIsInstance(self.sdk.store(), user_type)
        self.assertIsInstance(self.sdk.pos(), user_type)


if __name__ == "__main__":
    unittest.main()