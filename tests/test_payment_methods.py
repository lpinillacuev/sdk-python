"""Unit tests for the PaymentMethods resource using a mock HTTP client."""
import unittest
from unittest.mock import MagicMock

from mercadopago import SDK
from mercadopago.http import HttpClient
from tests.base_client_test import BaseClientTest


class TestPaymentMethods(BaseClientTest):
    """Test Module: PaymentMethods"""

    def test_list_all(self):
        fixture = self.load_fixture("payment_methods_list_all.json")
        self.mock_get(fixture)
        result = self.sdk.payment_methods().list_all()
        self.assertEqual(200, result["status"])
        self.assertIsInstance(result["response"], list)
        self.assertGreater(len(result["response"]), 0)
        # Ensure at least one method has expected fields
        first = result["response"][0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.mock_http.get.assert_called_once()

    def test_get_installments(self):
        client = HttpClient()
        response = [{"payment_method_id": "visa", "payer_costs": []}]
        client.get = MagicMock(return_value={"status": 200, "response": response})
        sdk = SDK("TEST_TOKEN", http_client=client)

        result = sdk.payment_methods().get_installments(
            "visa", 1000.0, issuer_id="123", bin="411111"
        )

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        client.get.assert_called_once()
        kwargs = client.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v1/payment_methods/installments",
                         kwargs["url"])
        self.assertEqual({"payment_method_id": "visa", "amount": 1000.0,
                          "issuer_id": "123", "bin": "411111"}, kwargs["params"])


if __name__ == "__main__":
    unittest.main()
