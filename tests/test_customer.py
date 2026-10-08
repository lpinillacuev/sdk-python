"""Unit tests for the Customer resource using a mock HTTP client."""
import unittest
from unittest.mock import ANY

from tests.base_client_test import BaseClientTest


class TestCustomer(BaseClientTest):
    """Test Module: Customer"""

    def test_create(self):
        self.mock_post({"id": "customer-1"}, status=201)
        payload = {"email": "customer@example.com"}
        result = self.sdk.customer().create(payload)
        self.assertEqual(201, result["status"])
        self.mock_http.post.assert_called_once_with(
            url=ANY,
            data='{"email": "customer@example.com"}',
            params=None,
            headers=ANY,
            timeout=ANY,
            maxretries=ANY,
            retry_on=ANY,
        )

    def test_get(self):
        self.mock_get({"id": "customer-1"})
        self.sdk.customer().get("customer/1")
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith(
            "/v1/customers/customer%2F1"
        ))

    def test_update(self):
        self.mock_put({"id": "customer-1"})
        self.sdk.customer().update("customer-1", {"last_name": "Updated"})
        self.assertTrue(self.mock_http.put.call_args.kwargs["url"].endswith(
            "/v1/customers/customer-1"
        ))

    def test_delete_uses_nonstandard_uri(self):
        self.mock_delete({"id": "customer-1"}, status=200)
        self.sdk.customer().delete("customer/1")
        self.assertTrue(self.mock_http.delete.call_args.kwargs["url"].endswith(
            "/v1/customers/customer%2F1/delete"
        ))

    def test_search(self):
        self.mock_get({"paging": {}, "results": []})
        result = self.sdk.customer().search({"email": "customer@example.com"})
        self.assertIsInstance(result["response"]["results"], list)
        self.assertEqual(
            {"email": "customer@example.com"},
            self.mock_http.get.call_args.kwargs["params"],
        )

    def test_create_address(self):
        self.mock_post({"zip_code": "01310-100"}, status=201)
        self.sdk.customer().create_address(
            "customer/1", {"zip_code": "01310-100"}
        )
        call = self.mock_http.post.call_args.kwargs
        self.assertTrue(call["url"].endswith(
            "/v1/customers/customer%2F1/addresses"
        ))
        self.assertEqual('{"zip_code": "01310-100"}', call["data"])

    def test_list_addresses_returns_list(self):
        self.mock_get([{"zip_code": "01310-100"}])
        result = self.sdk.customer().list_addresses("customer-1")
        self.assertIsInstance(result["response"], list)
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith(
            "/v1/customers/customer-1/addresses"
        ))

    def test_get_address(self):
        self.mock_get({"zip_code": "01310-100"})
        self.sdk.customer().get_address("customer/1", "address/1")
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith(
            "/v1/customers/customer%2F1/addresses/address%2F1"
        ))

    def test_update_address(self):
        self.mock_put({"zip_code": "01311-000"})
        self.sdk.customer().update_address(
            "customer-1", "address-1", {"zip_code": "01311-000"}
        )
        call = self.mock_http.put.call_args.kwargs
        self.assertTrue(call["url"].endswith(
            "/v1/customers/customer-1/addresses/address-1"
        ))
        self.assertEqual('{"zip_code": "01311-000"}', call["data"])

    def test_delete_address(self):
        self.mock_delete({}, status=200)
        self.sdk.customer().delete_address("customer-1", "address-1")
        self.assertTrue(self.mock_http.delete.call_args.kwargs["url"].endswith(
            "/v1/customers/customer-1/addresses/address-1"
        ))

    def test_request_objects_must_be_dicts(self):
        with self.assertRaises(ValueError):
            self.sdk.customer().create("not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.customer().update("customer-1", "not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.customer().create_address("customer-1", "not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.customer().update_address(
                "customer-1", "address-1", "not-a-dict"
            )


if __name__ == "__main__":
    unittest.main()