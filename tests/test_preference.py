"""Unit tests for the Preference resource using a mock HTTP client."""
import json
import unittest
import warnings

from mercadopago.config import RequestOptions
from tests.base_client_test import BaseClientTest


class TestPreference(BaseClientTest):
    """Test Module: Preference"""

    def test_create(self):
        fixture = self.load_fixture("preference_create.json")
        self.mock_post(fixture, status=201)
        preference_object = {
            "items": [{"title": "Point Mini", "quantity": 1, "unit_price": 58.80}]
        }
        request_options = RequestOptions(access_token="OTHER_TOKEN")
        result = self.sdk.preference().create(
            preference_object=preference_object, request_options=request_options
        )
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
        call = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/checkout/preferences", call["url"])
        self.assertEqual(preference_object, json.loads(call["data"]))
        self.assertEqual("Bearer OTHER_TOKEN", call["headers"]["Authorization"])

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
        request_options = RequestOptions(access_token="OTHER_TOKEN")
        result = self.sdk.preference().get(
            preference_id="pref/id", request_options=request_options
        )
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
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/checkout/preferences/pref%2Fid", call["url"])
        self.assertIsNone(call["params"])
        self.assertEqual("Bearer OTHER_TOKEN", call["headers"]["Authorization"])

    def test_update(self):
        fixture = self.load_fixture("preference_update.json")
        self.mock_put(fixture)
        preference_object = {"items": [{"title": "Updated Item"}]}
        request_options = RequestOptions(access_token="OTHER_TOKEN")
        result = self.sdk.preference().update(
            preference_id="pref/id",
            preference_object=preference_object,
            request_options=request_options,
        )
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("843382748-18d90a57-a4ce-4718-bc17-1234567890", resp["id"])
        self.assertIn("items", resp)
        call = self.mock_http.put.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/checkout/preferences/pref%2Fid", call["url"])
        self.assertEqual(preference_object, json.loads(call["data"]))
        self.assertEqual("Bearer OTHER_TOKEN", call["headers"]["Authorization"])

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
        request_options = RequestOptions(access_token="OTHER_TOKEN")
        result = self.sdk.preference().search(filters, request_options)
        self.assertEqual(200, result["status"])
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/checkout/preferences/search", call["url"])
        self.assertEqual(filters, call["params"])
        self.assertEqual("Bearer OTHER_TOKEN", call["headers"]["Authorization"])

    def test_expire(self):
        fixture = self.load_fixture("preference_update.json")
        self.mock_put(fixture)
        request_options = RequestOptions(access_token="OTHER_TOKEN")

        result = self.sdk.preference().expire("pref/id", request_options)

        self.assertEqual(200, result["status"])
        call = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/checkout/preferences/pref%2Fid/expire",
            call["url"],
        )
        self.assertIsNone(call["data"])
        self.assertIsNone(call["params"])
        self.assertEqual("Bearer OTHER_TOKEN", call["headers"]["Authorization"])

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.preference().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.preference().update("843382748-18d90a57-a4ce-4718-bc17-1234567890", "not-a-dict")


if __name__ == "__main__":
    unittest.main()