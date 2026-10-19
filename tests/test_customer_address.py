"""Direct tests for the CustomerAddress resource."""
import json
import unittest

from mercadopago.resources import CustomerAddress
from tests.base_client_test import BaseClientTest


class TestCustomerAddress(BaseClientTest):
    """Check customer-address HTTP requests and responses."""

    def test_list_all(self):
        addresses = [{"zip_code": "01310-100", "street_name": "Av. Paulista"}]
        self.mock_get(addresses)
        resource = self.sdk.customer_address()
        self.assertIsInstance(resource, CustomerAddress)
        result = resource.list_all("customer/1")
        self.assertEqual(200, result["status"])
        self.assertEqual(addresses, result["response"])
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith("/v1/customers/customer%2F1/addresses"))
        self.assertIn("Authorization", kwargs["headers"])

    def test_create(self):
        address = {
            "zip_code": "01310-100", "street_name": "Av. Paulista",
            "street_number": "1000", "city": "São Paulo", "state": "SP",
            "country": "BR",
        }
        self.mock_post(address, status=201)
        result = self.sdk.customer_address().create("customer/1", address)
        self.assertEqual(201, result["status"])
        self.assertEqual(address, result["response"])
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith("/v1/customers/customer%2F1/addresses"))
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])
        self.mock_http.post.assert_called_once()

    def test_delete(self):
        self.mock_delete(None, status=200)
        result = self.sdk.customer_address().delete("customer/1", "address/2")
        self.assertEqual(200, result["status"])
        self.assertIsNone(result["response"])
        kwargs = self.mock_http.delete.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith(
            "/v1/customers/customer%2F1/addresses/address%2F2"))
        self.mock_http.delete.assert_called_once()

    def test_get(self):
        address = {"zip_code": "01310-100", "city": "São Paulo"}
        self.mock_get(address)
        result = self.sdk.customer_address().get("customer/1", "address/2")
        self.assertEqual(200, result["status"])
        self.assertEqual(address, result["response"])
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith(
            "/v1/customers/customer%2F1/addresses/address%2F2"))
        self.mock_http.get.assert_called_once()

    def test_update(self):
        address = {"zip_code": "01310-100", "street_number": "1001"}
        self.mock_put(address)
        result = self.sdk.customer_address().update("customer/1", "address/2", address)
        self.assertEqual(200, result["status"])
        self.assertEqual(address, result["response"])
        kwargs = self.mock_http.put.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith(
            "/v1/customers/customer%2F1/addresses/address%2F2"))
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])
        self.mock_http.put.assert_called_once()


if __name__ == "__main__":
    unittest.main()