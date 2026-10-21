"""Unit tests for the CustomerAddress resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestCustomerAddress(BaseClientTest):
    """Test Module: CustomerAddress"""

    def test_list_customer_addresses(self):
        self.mock_get({"status": 200, "response": []})

        result = self.sdk.customer_address().list_customer_addresses("customer/1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer%2F1/addresses",
            kwargs["url"],
        )
        self.assertEqual(200, result["status"])

    def test_create_customer_address(self):
        self.mock_post({"status": 201, "response": {"id": "address-1"}}, status=201)
        address = {"street_name": "Av. Paulista", "street_number": "1000"}

        result = self.sdk.customer_address().create_customer_address("customer-1", address)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses",
            kwargs["url"],
        )
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_get_customer_address(self):
        self.mock_get({"status": 200, "response": {"id": "address-1"}})

        result = self.sdk.customer_address().get_customer_address("customer-1", "address/1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses/address%2F1",
            kwargs["url"],
        )
        self.assertEqual(200, result["status"])

    def test_update_customer_address(self):
        self.mock_put({"status": 200, "response": {"id": "address-1"}})
        address = {"city": "São Paulo", "state": "SP"}

        result = self.sdk.customer_address().update_customer_address(
            "customer-1", "address-1", address
        )

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses/address-1",
            kwargs["url"],
        )
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()