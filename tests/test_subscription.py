"""Unit tests for the Subscription resource using a mock HTTP client."""
import unittest

from tests.base_client_test import BaseClientTest


class TestSubscription(BaseClientTest):
    """Test Module: Subscription"""

    def test_get(self):
        fixture = self.load_fixture("subscription_get.json")
        self.mock_get(fixture)
        result = self.sdk.subscription().get("2c938084726fca480172750000000003")
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("2c938084726fca480172750000000003", resp["id"])
        self.assertEqual("authorized", resp["status"])
        self.assertEqual("2c938084726fca480172750000000002", resp["preapproval_plan_id"])
        self.assertEqual("test_user@testuser.com", resp["payer_email"])
        self.assertEqual(123456789, resp["payer_id"])
        self.assertIn("auto_recurring", resp)
        self.assertEqual(29.90, resp["auto_recurring"]["transaction_amount"])
        self.assertEqual("BRL", resp["auto_recurring"]["currency_id"])
        self.assertIn("next_payment_date", resp)
        self.assertIn("date_created", resp)
        self.mock_http.get.assert_called_once()

    def test_create(self):
        fixture = self.load_fixture("subscription_create.json")
        self.mock_post(fixture, status=201)
        subscription_object = {
            "preapproval_plan_id": "2c938084726fca480172750000000002",
            "payer_email": "test_user@testuser.com",
            "card_token_id": "a78sd6f1a9s8d7f1a",
        }
        result = self.sdk.subscription().create(subscription_object)
        self.assertEqual(201, result["status"])
        resp = result["response"]
        self.assertEqual("2c938084726fca480172750000000003", resp["id"])
        self.assertEqual("pending", resp["status"])
        self.assertEqual("2c938084726fca480172750000000002", resp["preapproval_plan_id"])
        self.assertIn("auto_recurring", resp)
        self.assertIn("date_created", resp)
        self.mock_http.post.assert_called_once()

    def test_update(self):
        fixture = self.load_fixture("subscription_update.json")
        self.mock_put(fixture)
        result = self.sdk.subscription().update("2c938084726fca480172750000000003", {"status": "cancelled"})
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("2c938084726fca480172750000000003", resp["id"])
        self.assertEqual("cancelled", resp["status"])
        self.assertIn("last_modified", resp)
        self.mock_http.put.assert_called_once()

    def test_search(self):
        fixture = self.load_fixture("subscription_search.json")
        self.mock_get(fixture)
        result = self.sdk.subscription().search({"status": "authorized"})
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertIn("results", resp)
        self.assertEqual("2c938084726fca480172750000000003", resp["results"][0]["id"])
        self.assertEqual("authorized", resp["results"][0]["status"])
        self.assertEqual("test_user@testuser.com", resp["results"][0]["payer_email"])
        self.mock_http.get.assert_called_once()

    def test_export_uses_exact_filters_and_returns_raw_csv(self):
        filters = {
            "collector_id": 123456789,
            "preapproval_plan_id": "2c938084726fca480172750000000002",
            "status": "authorized",
            "sort": "last_modified",
        }
        csv_response = unittest.mock.Mock()
        csv_response.content = b"id,status\nsub-1,authorized\n"
        csv_response.text = "id,status\nsub-1,authorized\n"
        self.mock_http.get.return_value = csv_response

        result = self.sdk.subscription().export(filters)

        self.assertIs(csv_response, result)
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/preapproval/export", kwargs["url"])
        self.assertEqual(filters, kwargs["params"])
        self.assertEqual("text/csv", kwargs["headers"]["Accept"])
        self.assertEqual(b"id,status\nsub-1,authorized\n", result.content)

    def test_export_requires_collector_id(self):
        with self.assertRaises(ValueError):
            self.sdk.subscription().export({"status": "authorized"})

        self.mock_http.get.assert_not_called()

    def test_export_raises_for_non_dict_filters(self):
        with self.assertRaises(ValueError):
            self.sdk.subscription().export("collector_id=123456789")

        self.mock_http.get.assert_not_called()

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.subscription().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.subscription().update("2c938084726fca480172750000000003", "not-a-dict")


if __name__ == "__main__":
    unittest.main()
