"""Unit tests for the Preference resource using a mock HTTP client."""
import unittest
import warnings

from tests.base_client_test import BaseClientTest


class TestPreference(BaseClientTest):
    """Test Module: Preference"""

    OPERATIONS = (
        {
            "product": "Checkout Pro",
            "tag": "Preferences",
            "operation_id": "createPreference",
            "path": "/checkout/preferences",
            "http_method": "POST",
            "resource_file": "mercadopago/resources/preference.py",
            "class": "Preference",
            "python_method": "create",
            "http_call": "_post",
            "uri": "/checkout/preferences",
            "path_params": (),
            "query_params": (),
            "body": "preference_object -> data",
            "status": "aligned",
            "evidence": "test_create asserts URL and JSON request data",
        },
        {
            "product": "Checkout Pro",
            "tag": "Preferences",
            "operation_id": "getPreference",
            "path": "/checkout/preferences/{id}",
            "http_method": "GET",
            "resource_file": "mercadopago/resources/preference.py",
            "class": "Preference",
            "python_method": "get",
            "http_call": "_get",
            "uri": "/checkout/preferences/{preference_id}",
            "path_params": ("id",),
            "query_params": (),
            "body": None,
            "status": "aligned",
            "evidence": "test_get asserts the preference_id URL segment",
        },
        {
            "product": "Checkout Pro",
            "tag": "Preferences",
            "operation_id": "updatePreference",
            "path": "/checkout/preferences/{id}",
            "http_method": "PUT",
            "resource_file": "mercadopago/resources/preference.py",
            "class": "Preference",
            "python_method": "update",
            "http_call": "_put",
            "uri": "/checkout/preferences/{preference_id}",
            "path_params": ("id",),
            "query_params": (),
            "body": "preference_object -> data",
            "status": "aligned",
            "evidence": "test_update asserts URL and JSON request data",
        },
        {
            "product": "Checkout Pro",
            "tag": "Preferences",
            "operation_id": "searchPreferences",
            "path": "/checkout/preferences/search",
            "http_method": "GET",
            "resource_file": "mercadopago/resources/preference.py",
            "class": "Preference",
            "python_method": "search",
            "http_call": "_get",
            "uri": "/checkout/preferences/search",
            "path_params": (),
            "query_params": (
                "external_reference",
                "marketplace",
                "site_id",
                "sponsor_id",
                "limit",
                "offset",
            ),
            "body": None,
            "status": "aligned",
            "evidence": "test_search asserts all documented filters as params",
        },
        {
            "product": "Checkout Pro",
            "tag": "Preference",
            "operation_id": None,
            "path": "/checkout/preferences/{id}/expire",
            "http_method": "PUT",
            "resource_file": "mercadopago/resources/preference.py",
            "class": "Preference",
            "python_method": "expire",
            "http_call": "_put",
            "uri": "/checkout/preferences/{preference_id}/expire",
            "path_params": ("id",),
            "query_params": (),
            "body": None,
            "status": "aligned",
            "evidence": "test_expire asserts URL, PUT call, and absent data",
        },
    )

    def test_openapi_operation_coverage(self):
        coverage = {
            "assigned_operations": 5,
            "verified_operations": len(self.OPERATIONS),
            "aligned_operations": sum(
                operation["status"] == "aligned" for operation in self.OPERATIONS
            ),
            "missing_operations": sum(
                operation["status"] == "missing" for operation in self.OPERATIONS
            ),
            "mismatched_operations": sum(
                operation["status"] == "mismatch" for operation in self.OPERATIONS
            ),
            "unverified_operations": sum(
                operation["status"] == "unverified" for operation in self.OPERATIONS
            ),
        }

        self.assertEqual(5, coverage["assigned_operations"])
        self.assertEqual(5, coverage["verified_operations"])
        self.assertEqual(5, coverage["aligned_operations"])
        self.assertEqual(0, coverage["missing_operations"])
        self.assertEqual(0, coverage["mismatched_operations"])
        self.assertEqual(0, coverage["unverified_operations"])
        self.assertIsNone(self.OPERATIONS[-1]["operation_id"])
        required_fields = {
            "product",
            "tag",
            "operation_id",
            "path",
            "http_method",
            "resource_file",
            "class",
            "python_method",
            "http_call",
            "uri",
            "path_params",
            "query_params",
            "body",
            "status",
            "evidence",
        }
        for operation in self.OPERATIONS:
            self.assertEqual(required_fields, set(operation))

    def test_create(self):
        fixture = self.load_fixture("preference_create.json")
        self.mock_post(fixture, status=201)
        preference_object = {
            "items": [{"title": "Point Mini", "quantity": 1, "unit_price": 58.80}]
        }
        result = self.sdk.preference().create(preference_object)
        self.assertEqual(201, result["status"])
        resp = result["response"]
        self.assertEqual("843382748-18d90a57-a4ce-4718-bc17-1234567890", resp["id"])
        self.assertIn("init_point", resp)
        self.assertIsInstance(resp["items"], list)
        self.assertEqual("Point Mini", resp["items"][0]["title"])
        self.assertEqual(843382748, resp["collector_id"])
        self.assertIn("back_urls", resp)
        self.assertIn("payment_methods", resp)
        self.assertEqual(12, resp["payment_methods"]["installments"])
        self.mock_http.post.assert_called_once()
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/checkout/preferences", request["url"]
        )
        self.assertEqual(preference_object, __import__("json").loads(request["data"]))

    def test_create_with_notification_url_warns(self):
        fixture = self.load_fixture("preference_create.json")
        self.mock_post(fixture, status=201)
        preference_object = {
            "items": [{"title": "Point Mini", "quantity": 1, "unit_price": 58.80}],
            "notification_url": "https://example.com/notify",
        }
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            self.sdk.preference().create(preference_object)
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))

    def test_get(self):
        fixture = self.load_fixture("preference_get.json")
        self.mock_get(fixture)
        result = self.sdk.preference().get("843382748-18d90a57-a4ce-4718-bc17-1234567890")
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("843382748-18d90a57-a4ce-4718-bc17-1234567890", resp["id"])
        self.assertIn("init_point", resp)
        self.assertIsInstance(resp["items"], list)
        self.assertEqual("Point Mini", resp["items"][0]["title"])
        self.assertEqual(58.80, resp["items"][0]["unit_price"])
        self.assertEqual(843382748, resp["collector_id"])
        self.assertIn("back_urls", resp)
        self.assertEqual("https://example.com/success", resp["back_urls"]["success"])
        self.assertEqual("MP-PREF-001", resp["external_reference"])
        self.assertIn("date_created", resp)
        self.mock_http.get.assert_called_once()
        request = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/checkout/preferences/"
            "843382748-18d90a57-a4ce-4718-bc17-1234567890",
            request["url"],
        )

    def test_update(self):
        fixture = self.load_fixture("preference_update.json")
        self.mock_put(fixture)
        result = self.sdk.preference().update(
            "843382748-18d90a57-a4ce-4718-bc17-1234567890",
            {"items": [{"title": "Updated Item"}]},
        )
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("843382748-18d90a57-a4ce-4718-bc17-1234567890", resp["id"])
        self.assertIn("items", resp)
        self.mock_http.put.assert_called_once()
        request = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/checkout/preferences/"
            "843382748-18d90a57-a4ce-4718-bc17-1234567890",
            request["url"],
        )
        self.assertEqual(
            {"items": [{"title": "Updated Item"}]},
            __import__("json").loads(request["data"]),
        )

    def test_search(self):
        fixture = self.load_fixture("preference_search.json")
        self.mock_get(fixture)
        filters = {
            "external_reference": "MP-PREF-001",
            "marketplace": "NONE",
            "site_id": "MLB",
            "sponsor_id": 123,
            "limit": 10,
            "offset": 20,
        }
        result = self.sdk.preference().search(filters)
        self.assertEqual(200, result["status"])
        self.mock_http.get.assert_called_once()
        request = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/checkout/preferences/search",
            request["url"],
        )
        self.assertEqual(filters, request["params"])

    def test_expire(self):
        fixture = self.load_fixture("preference_update.json")
        self.mock_put(fixture)
        result = self.sdk.preference().expire(
            "843382748-18d90a57-a4ce-4718-bc17-1234567890"
        )
        self.assertEqual(200, result["status"])
        self.mock_http.put.assert_called_once()
        request = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/checkout/preferences/"
            "843382748-18d90a57-a4ce-4718-bc17-1234567890/expire",
            request["url"],
        )
        self.assertIsNone(request["data"])
        self.assertIsNone(request["params"])

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.preference().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.preference().update("843382748-18d90a57-a4ce-4718-bc17-1234567890", "not-a-dict")


if __name__ == "__main__":
    unittest.main()
