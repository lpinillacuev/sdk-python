"""Unit tests for the POS resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestPOS(BaseClientTest):
    """Test Module: POS"""

    def test_list_pos(self):
        self.mock_get({"results": [{"id": 1}]})

        result = self.sdk.pos().list_pos("user/123")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/user%2F123/pos", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_search_pos(self):
        self.mock_get({"results": [{"id": 1}]})
        filters = {
            "external_id": "POS001",
            "external_store_id": "SUC001",
            "store_id": "1234567",
            "category": 621102,
        }

        result = self.sdk.pos().search_pos(filters=filters)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/pos", kwargs["url"])
        self.assertEqual(filters, kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_create_pos(self):
        self.mock_post({"id": 1}, status=201)
        payload = {
            "external_id": "POS001",
            "external_store_id": "SUC001",
            "fixed_amount": False,
            "name": "Main POS",
            "store_id": "1234567",
        }

        result = self.sdk.pos().create_pos(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/pos", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_delete_pos(self):
        self.mock_delete({"id": "pos-1"}, status=200)

        result = self.sdk.pos().delete_pos("pos-1")

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos-1", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_pos(self):
        self.mock_get({"id": "pos-1"})

        result = self.sdk.pos().get_pos("pos-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos-1", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_update_pos(self):
        self.mock_put({"id": "pos-1"})
        payload = {"external_id": "POS001", "name": "Updated POS"}

        result = self.sdk.pos().update_pos("pos-1", payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos-1", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()