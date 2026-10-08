"""Unit tests for the User resource using a mock HTTP client."""
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
        self.assertEqual("https://api.mercadopago.com/users/me",
                         self.mock_http.get.call_args.kwargs["url"])

    def test_create_store_forwards_dictionary_body_and_encodes_user_id(self):
        self.mock_post({})
        body = {"name": "Main", "external_id": "branch"}
        self.sdk.user().create_store("user/id", body)
        self.assertEqual(
            "https://api.mercadopago.com/users/user%2Fid/stores",
            self.mock_http.post.call_args.kwargs["url"],
        )
        self.assertEqual('{"name": "Main", "external_id": "branch"}',
                         self.mock_http.post.call_args.kwargs["data"])

    def test_search_stores_forwards_all_published_filters(self):
        self.mock_get({})
        filters = {"external_id": "branch"}
        self.sdk.user().search_stores("user/id", filters)
        self.assertEqual(
            "https://api.mercadopago.com/users/user%2Fid/stores/search",
            self.mock_http.get.call_args.kwargs["url"],
        )
        self.assertEqual(filters, self.mock_http.get.call_args.kwargs["params"])

    def test_get_store_uses_encoded_store_id(self):
        self.mock_get({})
        self.sdk.user().get_store("store/id")
        self.assertEqual(
            "https://api.mercadopago.com/stores/store%2Fid",
            self.mock_http.get.call_args.kwargs["url"],
        )

    def test_update_store_forwards_dictionary_body_and_encodes_ids(self):
        self.mock_put({})
        body = {"name": "Updated", "business_hours": {}}
        self.sdk.user().update_store("user/id", "store/id", body)
        self.assertEqual(
            "https://api.mercadopago.com/users/user%2Fid/stores/store%2Fid",
            self.mock_http.put.call_args.kwargs["url"],
        )
        self.assertEqual('{"name": "Updated", "business_hours": {}}',
                         self.mock_http.put.call_args.kwargs["data"])

    def test_delete_store_uses_encoded_path_parameters(self):
        self.mock_delete({})
        self.sdk.user().delete_store("user/id", "store/id")
        self.assertEqual(
            "https://api.mercadopago.com/users/user%2Fid/stores/store%2Fid",
            self.mock_http.delete.call_args.kwargs["url"],
        )

    def test_search_pos_forwards_all_published_filters(self):
        self.mock_get({})
        filters = {
            "external_id": "checkout",
            "external_store_id": "branch",
            "store_id": "store",
            "category": 621102,
        }
        self.sdk.user().search_pos(filters)
        self.assertEqual("https://api.mercadopago.com/pos",
                         self.mock_http.get.call_args.kwargs["url"])
        self.assertEqual(filters, self.mock_http.get.call_args.kwargs["params"])

    def test_create_pos_forwards_dictionary_body(self):
        self.mock_post({})
        body = {"name": "Checkout", "store_id": "store"}
        self.sdk.user().create_pos(body)
        self.assertEqual("https://api.mercadopago.com/pos",
                         self.mock_http.post.call_args.kwargs["url"])
        self.assertEqual('{"name": "Checkout", "store_id": "store"}',
                         self.mock_http.post.call_args.kwargs["data"])

    def test_get_pos_uses_encoded_pos_id(self):
        self.mock_get({})
        self.sdk.user().get_pos("pos/id")
        self.assertEqual("https://api.mercadopago.com/pos/pos%2Fid",
                         self.mock_http.get.call_args.kwargs["url"])

    def test_update_pos_forwards_dictionary_body_and_encodes_pos_id(self):
        self.mock_put({})
        body = {"name": "Updated", "fixed_amount": True}
        self.sdk.user().update_pos("pos/id", body)
        self.assertEqual("https://api.mercadopago.com/pos/pos%2Fid",
                         self.mock_http.put.call_args.kwargs["url"])
        self.assertEqual('{"name": "Updated", "fixed_amount": true}',
                         self.mock_http.put.call_args.kwargs["data"])

    def test_delete_pos_uses_encoded_pos_id(self):
        self.mock_delete({})
        self.sdk.user().delete_pos("pos/id")
        self.assertEqual("https://api.mercadopago.com/pos/pos%2Fid",
                         self.mock_http.delete.call_args.kwargs["url"])

    def test_list_pos_uses_encoded_user_id(self):
        self.mock_get({})
        self.sdk.user().list_pos("user/id")
        self.assertEqual(
            "https://api.mercadopago.com/users/user%2Fid/pos",
            self.mock_http.get.call_args.kwargs["url"],
        )


if __name__ == "__main__":
    unittest.main()
