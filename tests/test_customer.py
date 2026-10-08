"""Unit tests for the Customer resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestCustomer(BaseClientTest):
    """Test Module: Customer"""

    def test_create(self):
        fixture = self.load_fixture("customer_create.json")
        self.mock_post(fixture, status=201)
        customer_object = {
            "email": "test_user@testuser.com",
            "first_name": "Test",
            "last_name": "User",
            "phone": {"area_code": "11", "number": "987654321"},
            "identification": {"type": "CPF", "number": "19119119100"},
        }
        result = self.sdk.customer().create(customer_object)
        self.assertEqual(201, result["status"])
        resp = result["response"]
        self.assertEqual("1068193981-pXRewrKqlP6pnn", resp["id"])
        self.assertEqual("test_user@testuser.com", resp["email"])
        self.assertEqual("Test", resp["first_name"])
        self.assertEqual("User", resp["last_name"])
        self.assertIn("phone", resp)
        self.assertIn("identification", resp)
        self.assertEqual("CPF", resp["identification"]["type"])
        self.assertIn("date_created", resp)
        self.mock_http.post.assert_called_once()
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers", request["url"]
        )
        self.assertEqual(customer_object, json.loads(request["data"]))

    def test_get(self):
        fixture = self.load_fixture("customer_get.json")
        self.mock_get(fixture)
        result = self.sdk.customer().get("1068193981-pXRewrKqlP6pnn")
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("1068193981-pXRewrKqlP6pnn", resp["id"])
        self.assertEqual("test_user@testuser.com", resp["email"])
        self.assertEqual("Test", resp["first_name"])
        self.assertEqual("User", resp["last_name"])
        self.assertIn("phone", resp)
        self.assertEqual("11", resp["phone"]["area_code"])
        self.assertIn("identification", resp)
        self.assertEqual("CPF", resp["identification"]["type"])
        self.assertIn("address", resp)
        self.assertIn("date_created", resp)
        self.assertIn("date_last_updated", resp)
        self.assertIsInstance(resp["cards"], list)
        self.mock_http.get.assert_called_once()
        request = self.mock_http.get.call_args.kwargs
        self.assertTrue(
            request["url"].endswith(
                "/v1/customers/1068193981-pXRewrKqlP6pnn"
            )
        )

    def test_update(self):
        fixture = self.load_fixture("customer_update.json")
        self.mock_put(fixture)
        result = self.sdk.customer().update("1068193981-pXRewrKqlP6pnn", {"last_name": "Updated"})
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("1068193981-pXRewrKqlP6pnn", resp["id"])
        self.assertEqual("Updated", resp["last_name"])
        self.assertIn("date_last_updated", resp)
        self.mock_http.put.assert_called_once()
        request = self.mock_http.put.call_args.kwargs
        self.assertTrue(
            request["url"].endswith(
                "/v1/customers/1068193981-pXRewrKqlP6pnn"
            )
        )
        self.assertEqual({"last_name": "Updated"}, json.loads(request["data"]))

    def test_delete(self):
        fixture = self.load_fixture("customer_delete.json")
        self.mock_delete(fixture, status=200)
        result = self.sdk.customer().delete("1068193981-pXRewrKqlP6pnn")
        self.assertEqual(200, result["status"])
        self.mock_http.delete.assert_called_once()
        request = self.mock_http.delete.call_args.kwargs
        self.assertTrue(
            request["url"].endswith(
                "/v1/customers/1068193981-pXRewrKqlP6pnn/delete"
            )
        )

    def test_search(self):
        fixture = self.load_fixture("customer_search.json")
        self.mock_get(fixture)
        filters = {
            "email": "test_user@testuser.com",
            "limit": 30,
            "offset": 0,
        }
        result = self.sdk.customer().search(filters)
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertIn("results", resp)
        self.assertIn("paging", resp)
        self.assertEqual(1, resp["paging"]["total"])
        self.assertEqual("test_user@testuser.com", resp["results"][0]["email"])
        self.mock_http.get.assert_called_once()
        request = self.mock_http.get.call_args.kwargs
        self.assertTrue(request["url"].endswith("/v1/customers/search"))
        self.assertEqual(filters, request["params"])

    def test_address_operations(self):
        customer_id = "1068193981-pXRewrKqlP6pnn"
        address_id = "address-001"
        address = {"zip_code": "01310-100", "street_name": "Av. Paulista"}

        self.mock_post(address, status=201)
        self.sdk.customer().create_address(customer_id, address)
        self.mock_http.post.assert_called_once_with(
            url=("https://api.mercadopago.com/v1/customers/"
                 "1068193981-pXRewrKqlP6pnn/addresses"),
            data=json.dumps(address),
            params=None,
            headers=unittest.mock.ANY,
            timeout=60.0,
            maxretries=3,
            retry_on=None,
        )

        self.mock_http.reset_mock()
        self.mock_get([address])
        self.sdk.customer().list_addresses(customer_id)
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith(
            "/v1/customers/1068193981-pXRewrKqlP6pnn/addresses"))

        self.mock_http.reset_mock()
        self.mock_get(address)
        self.sdk.customer().get_address(customer_id, address_id)
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith(
            "/v1/customers/1068193981-pXRewrKqlP6pnn/addresses/address-001"))

        self.mock_http.reset_mock()
        self.mock_put(address)
        self.sdk.customer().update_address(customer_id, address_id, address)
        request = self.mock_http.put.call_args.kwargs
        self.assertTrue(request["url"].endswith(
            "/v1/customers/1068193981-pXRewrKqlP6pnn/addresses/address-001"))
        self.assertEqual(address, json.loads(request["data"]))

        self.mock_http.reset_mock()
        self.mock_delete({}, status=200)
        self.sdk.customer().delete_address(customer_id, address_id)
        self.assertTrue(self.mock_http.delete.call_args.kwargs["url"].endswith(
            "/v1/customers/1068193981-pXRewrKqlP6pnn/addresses/address-001"))

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.customer().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.customer().update("1068193981-pXRewrKqlP6pnn", "not-a-dict")

    def test_address_writes_raise_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.customer().create_address("customer-id", "not-a-dict")
        with self.assertRaises(ValueError):
            self.sdk.customer().update_address(
                "customer-id", "address-id", "not-a-dict")


if __name__ == "__main__":
    unittest.main()
