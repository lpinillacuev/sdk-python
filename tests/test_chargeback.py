"""Unit tests for the Chargeback resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestChargeback(BaseClientTest):
    """Test Module: Chargeback"""

    def test_get(self):
        fixture = self.load_fixture("chargeback_get.json")
        self.mock_get(fixture)
        result = self.sdk.chargeback().get("cb-001")
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("cb-001", resp["id"])
        self.assertEqual(17014025134, resp["payment_id"])
        self.assertEqual(58.80, resp["amount"])
        self.assertEqual("in_process", resp["status"])
        self.assertEqual("BRL", resp["currency_id"])
        self.assertIn("date_created", resp)
        self.mock_http.get.assert_called_once()

    def test_search(self):
        fixture = self.load_fixture("chargeback_search.json")
        self.mock_get(fixture)
        result = self.sdk.chargeback().search({"payment_id": 17014025134})
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertIn("results", resp)
        self.assertEqual("cb-001", resp["results"][0]["id"])
        self.assertEqual(17014025134, resp["results"][0]["payment_id"])
        self.mock_http.get.assert_called_once()

    def test_update_chargeback(self):
        payload = {"files": [{"name": "receipt", "description": "Receipt",
                              "url": "https://example.com/receipt.pdf"}]}
        self.mock_put({"id": "cb-001"})

        result = self.sdk.chargeback().update_chargeback("cb-001", payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/chargebacks/cb-001", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()
