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
        # Ensure at least one method has expected fields
        first = result["response"][0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.mock_http.get.assert_called_once()

    def test_get_installments_with_required_filters(self):
        fixture = self.load_fixture("payment_methods_list_all.json")
        self.mock_get(fixture)

        self.sdk.payment_methods().get_installments("visa", 100)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            {"payment_method_id": "visa", "amount": 100},
            kwargs["params"],
        )

    def test_get_installments_with_optional_filters(self):
        fixture = self.load_fixture("payment_methods_list_all.json")
        self.mock_get(fixture)

        self.sdk.payment_methods().get_installments(
            "visa", 100, issuer_id="123", bin="411111"
        )

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            {
                "payment_method_id": "visa",
                "amount": 100,
                "issuer_id": "123",
                "bin": "411111",
            },
            kwargs["params"],
        )


if __name__ == "__main__":
    unittest.main()
