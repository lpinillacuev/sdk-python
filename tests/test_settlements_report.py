"""Unit tests for the SettlementsReport resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestSettlementsReport(BaseClientTest):
    """Test Module: SettlementsReport"""

    def test_search_settlement_reports(self):
        filters = {"begin_date": "2025-01-01T00:00:00Z", "end_date": "2025-01-31T00:00:00Z"}
        self.mock_get({"results": []})

        result = self.sdk.settlements_report().search_settlement_reports(filters)

        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/search",
            kwargs["url"],
        )
        self.assertEqual(filters, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_download_settlement_report(self):
        csv_bytes = b"id,amount\n1,100\n"
        self.mock_http.get_binary.return_value = {
            "status": 200, "response": csv_bytes,
        }

        result = self.sdk.settlements_report().download_settlement_report("report.csv")

        self.mock_http.get_binary.assert_called_once()
        kwargs = self.mock_http.get_binary.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/report.csv",
            kwargs["url"],
        )
        self.assertEqual(200, result["status"])
        self.assertEqual(csv_bytes, result["response"])

    def test_get_settlement_report_task(self):
        self.mock_get({"id": "task-1"})

        result = self.sdk.settlements_report().get_settlement_report_task("task-1")

        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/task/task-1",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_settlement_report(self):
        self.mock_get({"results": []})

        result = self.sdk.settlements_report().get_settlement_report()

        self.mock_http.get.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report",
            self.mock_http.get.call_args.kwargs["url"],
        )
        self.assertEqual(200, result["status"])

    def test_create_settlement_report(self):
        payload = {"date_from": "2025-01-01", "date_to": "2025-01-31"}
        self.mock_post({"id": "task-1"})

        result = self.sdk.settlements_report().create_settlement_report(payload)

        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_get_settlement_report_config(self):
        self.mock_get({"columns": []})

        result = self.sdk.settlements_report().get_settlement_report_config()

        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/config",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_settlement_report_config(self):
        payload = {"columns": ["DATE", "TRANSACTION_ID"]}
        self.mock_post({"columns": payload["columns"]})

        result = self.sdk.settlements_report().create_settlement_report_config(payload)

        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/config",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()