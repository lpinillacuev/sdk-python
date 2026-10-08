"""Unit tests for the PaymentMethods resource using a mock HTTP client."""
import unittest

from tests.base_client_test import BaseClientTest


class TestPaymentMethods(BaseClientTest):
    """Test Module: PaymentMethods"""

    def test_list_all_uses_exact_catalog_path_without_query(self):
        fixture = self.load_fixture("payment_methods_list_all.json")
        self.mock_get(fixture)
        result = self.sdk.payment_methods().list_all()
        self.assertEqual(200, result["status"])
        self.assertIsInstance(result["response"], list)
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v1/payment_methods", call["url"])
        self.assertIsNone(call["params"])
        self.assertIn("Authorization", call["headers"])

    def test_get_installments_sends_required_and_optional_query_arguments(self):
        self.mock_get([])
        result = self.sdk.payment_methods().get_installments(
            "visa", 1000.0, issuer_id="310", bin="411111"
        )
        self.assertEqual(200, result["status"])
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/payment_methods/installments",
            call["url"],
        )
        self.assertEqual(
            {
                "payment_method_id": "visa",
                "amount": 1000.0,
                "issuer_id": "310",
                "bin": "411111",
            },
            call["params"],
        )
        self.assertIn("Authorization", call["headers"])

    def test_get_installments_omits_absent_optional_query_arguments(self):
        self.mock_get([])
        self.sdk.payment_methods().get_installments("visa", 1000.0)
        self.assertEqual(
            {"payment_method_id": "visa", "amount": 1000.0},
            self.mock_http.get.call_args.kwargs["params"],
        )


if __name__ == "__main__":
    unittest.main()