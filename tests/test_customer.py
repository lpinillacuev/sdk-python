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

    def test_delete_uses_encoded_customer_id_and_delete_suffix(self):
        fixture = self.load_fixture("customer_delete.json")
        self.mock_delete(fixture, status=200)
        result = self.sdk.customer().delete("customer/id with space")
        self.assertEqual(200, result["status"])
        self.mock_http.delete.assert_called_once()
        call = self.mock_http.delete.call_args.kwargs
        self.assertTrue(call["url"].endswith(
            "/v1/customers/customer%2Fid%20with%20space/delete"
        ))

    def test_card_create_uses_encoded_customer_id_without_trailing_slash(self):
        fixture = self.load_fixture("card_create.json")
        self.mock_post(fixture, status=201)
        card_object = {"token": "card-token"}
        result = self.sdk.card().create("customer/id with space", card_object)
        self.assertEqual(201, result["status"])
        self.mock_http.post.assert_called_once()
        call = self.mock_http.post.call_args.kwargs
        self.assertTrue(call["url"].endswith(
            "/v1/customers/customer%2Fid%20with%20space/cards"
        ))
        self.assertFalse(call["url"].endswith("/"))
        self.assertEqual(card_object, json.loads(call["data"]))

    def test_search(self):
        fixture = self.load_fixture("customer_search.json")
        self.mock_get(fixture)
        result = self.sdk.customer().search({"email": "test_user@testuser.com"})
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertIn("results", resp)
        self.assertIn("paging", resp)
        self.assertEqual(1, resp["paging"]["total"])
        self.assertEqual("test_user@testuser.com", resp["results"][0]["email"])
        self.mock_http.get.assert_called_once()

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.customer().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.customer().update("1068193981-pXRewrKqlP6pnn", "not-a-dict")


if __name__ == "__main__":
    unittest.main()