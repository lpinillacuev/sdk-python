"""Direct tests for the settlement report SDK resource."""
import json
import unittest
from unittest.mock import MagicMock, patch

from mercadopago.sdk import SDK
from mercadopago.resources.settlement_report import SettlementReport
from mercadopago.http.http_client import HttpClient
from mercadopago.errors.exceptions import MPServerError

from tests.base_client_test import BaseClientTest


class TestSettlementReport(BaseClientTest):
    """Verify HTTP verbs, paths, and payloads of all report operations."""

    def check_call(self, verb, path, response, status=200):
        """Assert that a resource call reached the expected transport route."""
        self.assertEqual(status, response["status"])
        self.assertEqual(self.sdk.settlement_report().config.api_base_url + path,
                         getattr(self.mock_http, verb).call_args.kwargs["url"])

    def test_get_settlement_report(self):
        self.mock_get({"results": []})
        result = self.sdk.settlement_report().get_settlement_report()
        self.check_call("get", "/v1/account/settlement_report", result)
        self.assertEqual({"results": []}, result["response"])

    def test_create_settlement_report(self):
        data = {"begin_date": "2025-01-01T00:00:00Z", "end_date": "2025-01-02T00:00:00Z"}
        self.mock_post({"id": "task-1"}, status=202)
        result = self.sdk.settlement_report().create_settlement_report(data)
        self.check_call("post", "/v1/account/settlement_report", result, 202)
        self.assertEqual(data, json.loads(self.mock_http.post.call_args.kwargs["data"]))
        self.assertEqual({"id": "task-1"}, result["response"])

    def test_get_settlement_report_config(self):
        self.mock_get({"frequency": "daily"})
        result = self.sdk.settlement_report().get_settlement_report_config()
        self.check_call("get", "/v1/account/settlement_report/config", result)
        self.assertEqual("daily", result["response"]["frequency"])

    def test_create_settlement_report_config(self):
        data = {"frequency": "daily"}
        self.mock_post(data)
        result = self.sdk.settlement_report().create_settlement_report_config(data)
        self.check_call("post", "/v1/account/settlement_report/config", result)
        self.assertEqual(data, json.loads(self.mock_http.post.call_args.kwargs["data"]))
        self.assertEqual(data, result["response"])

    def test_update_settlement_report_config(self):
        data = {"frequency": "monthly"}
        self.mock_put(data)
        result = self.sdk.settlement_report().update_settlement_report_config(data)
        self.check_call("put", "/v1/account/settlement_report/config", result)
        self.assertEqual(data, json.loads(self.mock_http.put.call_args.kwargs["data"]))
        self.assertEqual(data, result["response"])

    def test_list_scheduled_settlement_reports(self):
        self.mock_get({"results": []})
        result = self.sdk.settlement_report().list_scheduled_settlement_reports()
        self.check_call("get", "/v1/account/settlement_report/list", result)
        self.assertEqual([], result["response"]["results"])

    def test_disable_settlement_report_schedule(self):
        self.mock_http.delete.return_value = {"status": 200, "response": None}
        result = self.sdk.settlement_report().disable_settlement_report_schedule()
        self.check_call("delete", "/v1/account/settlement_report/schedule", result)
        self.assertIsNone(result["response"])

    def test_enable_settlement_report_schedule(self):
        self.mock_http.post.return_value = {"status": 200, "response": None}
        result = self.sdk.settlement_report().enable_settlement_report_schedule()
        self.check_call("post", "/v1/account/settlement_report/schedule", result)
        self.assertIsNone(self.mock_http.post.call_args.kwargs["data"])
        self.assertIsNone(result["response"])

    def test_search_settlement_reports(self):
        filters = {"begin_date": "2025-01-01T00:00:00Z", "end_date": "2025-02-01T00:00:00Z"}
        self.mock_get({"results": []})
        result = self.sdk.settlement_report().search_settlement_reports(filters)
        self.check_call("get", "/v1/account/settlement_report/search", result)
        self.assertEqual(filters, self.mock_http.get.call_args.kwargs["params"])

    def test_get_settlement_report_task(self):
        self.mock_get({"id": "a/b"})
        result = self.sdk.settlement_report().get_settlement_report_task("a/b")
        self.check_call("get", "/v1/account/settlement_report/task/a%2Fb", result)
        self.assertEqual("a/b", result["response"]["id"])

    def test_download_settlement_report(self):
        self.mock_http.get_binary.return_value = {"status": 200, "response": b"id;value\n1;\xff\n"}
        result = self.sdk.settlement_report().download_settlement_report("a/b.csv")
        self.assertEqual(b"id;value\n1;\xff\n", result["response"])
        self.assertEqual(200, result["status"])
        self.assertEqual(self.sdk.settlement_report().config.api_base_url +
                         "/v1/account/settlement_report/a%2Fb.csv",
                         self.mock_http.get_binary.call_args.kwargs["url"])

    def test_sdk_factory(self):
        self.assertIsInstance(self.sdk.settlement_report(), SettlementReport)
        self.assertIsInstance(SDK("token").settlement_report(), SettlementReport)


class TestSettlementReportBinaryTransport(unittest.TestCase):
    """CSV success and JSON error handling on the binary-only transport."""

    @patch("mercadopago.http.http_client.requests.Session")
    def test_csv_bytes_and_json_default(self, session_cls):
        session = session_cls.return_value.__enter__.return_value
        csv_response = MagicMock(status_code=200, content=b"id\n\xff\n")
        json_response = MagicMock(status_code=200, content=b'{"ok":true}')
        json_response.json.return_value = {"ok": True}
        session.request.side_effect = [csv_response, json_response]
        client = HttpClient()
        self.assertEqual(b"id\n\xff\n", client.get_binary("https://example.test", {} )["response"])
        self.assertEqual({"ok": True}, client.get("https://example.test", {})["response"])

    @patch("mercadopago.http.http_client.requests.Session")
    def test_csv_error_is_json(self, session_cls):
        session = session_cls.return_value.__enter__.return_value
        error = MagicMock(status_code=404, content=b'{"message":"missing"}')
        error.json.return_value = {"message": "missing"}
        session.request.return_value = error
        result = HttpClient().get_binary("https://example.test", {})
        self.assertEqual({"message": "missing"}, result["response"])

    @patch("mercadopago.http.http_client.requests.Session")
    def test_csv_error_invalid_json(self, session_cls):
        session = session_cls.return_value.__enter__.return_value
        error = MagicMock(status_code=500, content=b"bad")
        error.json.side_effect = ValueError("bad JSON")
        session.request.return_value = error
        with self.assertRaises(MPServerError):
            HttpClient().get_binary("https://example.test", {})


if __name__ == "__main__":
    unittest.main()