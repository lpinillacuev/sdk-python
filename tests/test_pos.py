"""Tests for searching and creating points of sale through the SDK."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestPOS(BaseClientTest):
    """Wire-level tests for the POS resource."""

    def test_list_pos(self):
        response = {"paging": {"total": 1, "limit": 30, "offset": 0},
                    "results": [{"id": "42", "name": "Main POS"}]}
        self.mock_get(response)

        result = self.sdk.pos().list_pos("123/456")

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/users/123%2F456/pos", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertEqual("application/json", kwargs["headers"]["Accept"])

    def test_search_pos(self):
        filters = {
            "external_id": "POS001",
            "external_store_id": "SUC001",
            "store_id": "1234567",
            "category": 621102,
        }
        response = {
            "paging": {"total": 1, "limit": 30, "offset": 0},
            "results": [{"id": "42", "name": "Main POS", "store_id": "1234567"}],
        }
        self.mock_get(response)

        result = self.sdk.pos().search_pos(filters)

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/pos", kwargs["url"])
        self.assertEqual(filters, kwargs["params"])
        self.assertEqual("application/json", kwargs["headers"]["Accept"])

    def test_create_pos(self):
        payload = {
            "name": "Main POS",
            "store_id": "1234567",
            "external_id": "POS001",
            "external_store_id": "SUC001",
            "category": 621102,
            "fixed_amount": False,
            "url": "https://example.com/webhook",
        }
        response = {"id": "42", "qr_code": "qr-data", **payload}
        self.mock_post(response, status=201)

        result = self.sdk.pos().create_pos(payload)

        self.assertEqual(201, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/pos", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])


if __name__ == "__main__":
    unittest.main()