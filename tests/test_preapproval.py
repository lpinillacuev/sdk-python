"""Unit tests for the PreApproval resource and CSV transport boundary."""
import unittest
from unittest.mock import Mock, patch

from mercadopago.http import HttpClient
from tests.base_client_test import BaseClientTest


class TestPreApproval(BaseClientTest):
    """Test Module: PreApproval"""

    def test_get(self):
        fixture = self.load_fixture("preapproval_get.json")
        self.mock_get(fixture)
        result = self.sdk.preapproval().get("2c938084726fca480172750000000000")
        self.assertEqual(200, result["status"])
        self.assertEqual("2c938084726fca480172750000000000", result["response"]["id"])
        self.mock_http.get.assert_called_once()

    def test_create(self):
        fixture = self.load_fixture("preapproval_create.json")
        self.mock_post(fixture, status=201)
        body = {
            "reason": "Monthly subscription",
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 29.90,
                "currency_id": "BRL",
            },
            "payer_email": "test_user@testuser.com",
        }
        result = self.sdk.preapproval().create(body)
        self.assertEqual(201, result["status"])
        self.mock_http.post.assert_called_once()

    def test_update(self):
        fixture = self.load_fixture("preapproval_update.json")
        self.mock_put(fixture)
        result = self.sdk.preapproval().update(
            "2c938084726fca480172750000000000", {"status": "cancelled"}
        )
        self.assertEqual("cancelled", result["response"]["status"])
        self.mock_http.put.assert_called_once()

    def test_search(self):
        fixture = self.load_fixture("preapproval_search.json")
        self.mock_get(fixture)
        result = self.sdk.preapproval().search({"status": "authorized"})
        self.assertIn("results", result["response"])
        self.mock_http.get.assert_called_once()

    def test_export_preserves_csv_bytes_and_filters(self):
        csv_content = b"id,status\nsubscription-1,authorized\n"
        response = Mock(status_code=200, content=csv_content)
        response.headers = {"Content-Type": "text/csv; charset=utf-8"}
        response.json.side_effect = ValueError("CSV is not JSON")

        with patch("mercadopago.http.http_client.requests.request", return_value=response):
            result = self.sdk.preapproval().export(
                123456789,
                preapproval_plan_id="plan-1",
                status="authorized",
                sort="last_modified",
            )

        self.assertEqual(200, result["status"])
        self.assertEqual(csv_content, result["response"])
        response.json.assert_not_called()

    def test_export_omits_optional_filters(self):
        self.mock_get(b"id,status\n")
        self.sdk.preapproval().export(123456789)
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual({"collector_id": 123456789}, kwargs["params"])

    def test_http_client_preserves_text_csv_bytes(self):
        csv_content = b"id,status\nsubscription-1,authorized\n"
        response = Mock(status_code=200, content=csv_content)
        response.headers = {"Content-Type": "text/csv"}
        response.json.side_effect = ValueError("CSV is not JSON")

        with patch("mercadopago.http.http_client.requests.request", return_value=response):
            result = HttpClient().get("https://api.example.test/preapproval/export")

        self.assertEqual(csv_content, result["response"])
        response.json.assert_not_called()

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.preapproval().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.preapproval().update("subscription-id", "not-a-dict")


if __name__ == "__main__":
    unittest.main()