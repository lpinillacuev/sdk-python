"""Unit tests for the Chargeback resource using a mock HTTP client."""
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
        import json
        from unittest.mock import MagicMock

        from mercadopago import SDK
        from mercadopago.http import HttpClient

        client = HttpClient()
        response = {"id": "cb-001", "status": "in_process"}
        client.put = MagicMock(return_value={"status": 200, "response": response})
        sdk = SDK("TEST_TOKEN", http_client=client)
        payload = {"files": [{"name": "evidence.pdf", "description": "Receipt",
                              "url": "https://example.com/evidence.pdf"}]}

        result = sdk.chargeback().update_chargeback("cb-001", payload)

        client.put.assert_called_once()
        self.assertFalse(client.get.called)
        kwargs = client.put.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v1/chargebacks/cb-001",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])
        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])



if __name__ == "__main__":
    unittest.main()
