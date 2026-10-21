"""Unit tests for the CustomerAddress resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestCustomerAddress(BaseClientTest):
    """Test Module: CustomerAddress"""

    def test_list_customer_addresses(self):
        self.mock_get([{"zip_code": "01310-100"}])

        result = self.sdk.customer_address().list_customer_addresses("customer/123")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer%2F123/addresses",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_create_customer_address(self):
        address = {
            "zip_code": "01310-100",
            "street_name": "Av. Paulista",
            "street_number": "1000",
            "city": "São Paulo",
            "state": "SP",
            "country": "BR",
        }
        self.mock_post(address, status=201)

        result = self.sdk.customer_address().create_customer_address(
            "customer/123", address,
        )

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer%2F123/addresses",
            kwargs["url"],
        )
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])


if __name__ == "__main__":
    unittest.main()