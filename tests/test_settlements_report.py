"""Unit tests for the SettlementsReport resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestSettlementsReport(BaseClientTest):
    """Test Module: SettlementsReport"""

    def test_get_settlement_report(self):
        self.mock_http.get.return_value = {
            "status": 200, "response": {"results": []},
        }

        result = self.sdk.settlements_report().get_settlement_report()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_settlement_report(self):
        self.mock_http.post.return_value = {
            "status": 202, "response": {"id": "1"},
        }
        payload = {
            "begin_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-01-31T23:59:59Z",
        }

        result = self.sdk.settlements_report().create_settlement_report(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(202, result["status"])

    def test_get_settlement_report_config(self):
        self.mock_http.get.return_value = {
            "status": 200, "response": {"frequency": {"type": "daily"}},
        }

        result = self.sdk.settlements_report().get_settlement_report_config()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/config",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_update_settlement_report_config(self):
        self.mock_http.put.return_value = {"status": 200, "response": {}}
        payload = {"frequency": {"type": "daily", "hour": 9}}
        result = self.sdk.settlements_report().update_settlement_report_config(payload)
        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/config",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_list_scheduled_settlement_reports(self):
        self.mock_http.get.return_value = {"status": 200, "response": {}}
        result = self.sdk.settlements_report().list_scheduled_settlement_reports()
        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/list",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_disable_settlement_report_schedule(self):
        self.mock_http.delete.return_value = {"status": 200, "response": None}
        result = self.sdk.settlements_report().disable_settlement_report_schedule()
        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/schedule",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_enable_settlement_report_schedule(self):
        self.mock_http.post.return_value = {"status": 200, "response": None}
        result = self.sdk.settlements_report().enable_settlement_report_schedule()
        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/schedule",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_search_settlement_reports(self):
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}
        begin_date = "2024-01-01T00:00:00Z"
        end_date = "2024-01-31T23:59:59Z"

        result = self.sdk.settlements_report().search_settlement_reports(
            begin_date=begin_date, end_date=end_date,
        )

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/search",
            kwargs["url"],
        )
        self.assertEqual(
            {"begin_date": begin_date, "end_date": end_date}, kwargs["params"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_settlement_report_task(self):
        self.mock_http.get.return_value = {"status": 200, "response": {"id": "task-1"}}

        result = self.sdk.settlements_report().get_settlement_report_task("task-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/task/task-1",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_settlement_report_config(self):
        self.mock_http.post.return_value = {
            "status": 200, "response": {"frequency": {"type": "daily"}},
        }
        payload = {
            "columns": [{"key": "DATE", "alias": "transaction_date"}],
            "frequency": {"type": "daily", "hour": 9},
            "file_name_prefix": "settlements_report",
        }

        result = self.sdk.settlements_report().create_settlement_report_config(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/settlement_report/config",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()