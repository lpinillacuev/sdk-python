"""Unit tests for the PaymentMethods resource using a mock HTTP client."""
import unittest

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
        first = result["response"][0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.mock_http.get.assert_called_once()
        call = self.mock_http.get.call_args.kwargs
        self.assertTrue(call["url"].endswith("/v1/payment_methods"))
        self.assertIsNone(call["params"])

    def test_get_installments_sends_documented_query(self):
        fixture = [{"payment_method_id": "visa", "payer_costs": []}]
        self.mock_get(fixture)
        filters = {
            "payment_method_id": "visa",
            "amount": 1000.0,
            "issuer_id": "310",
            "bin": "411111",
        }
        result = self.sdk.payment_methods().get_installments(filters)
        self.assertEqual(200, result["status"])
        call = self.mock_http.get.call_args.kwargs
        self.assertTrue(call["url"].endswith("/v1/payment_methods/installments"))
        self.assertEqual(filters, call["params"])

    def test_get_installments_requires_filters_dictionary(self):
        with self.assertRaises(ValueError):
            self.sdk.payment_methods().get_installments("visa")

    def test_get_installments_requires_payment_method_and_amount(self):
        with self.assertRaises(ValueError):
            self.sdk.payment_methods().get_installments({"payment_method_id": "visa"})


if __name__ == "__main__":
    unittest.main()