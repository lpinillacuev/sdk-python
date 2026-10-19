"""Direct request tests for the releases report resource."""
import json
import unittest
from unittest.mock import Mock, patch

from mercadopago.config.request_options import RequestOptions
from mercadopago.errors.exceptions import MPServerError
from mercadopago.http import HttpClient
from mercadopago.resources.release_report import ReleaseReport
from mercadopago.sdk import SDK


class TestReleaseReport(unittest.TestCase):
    """Verify report operations without making network requests."""

    def setUp(self):
        self.http = Mock(spec=HttpClient)
        self.sdk = SDK("test-token", http_client=self.http)
        self.report = self.sdk.release_report()
        self.root = self.report.config.api_base_url + "/v1/account/release_report"

    def check_request(self, verb, path, response, expected_status=200, **expected):
        """Check the verb, URL, authentication and returned envelope."""
        call = getattr(self.http, verb)
        call.return_value = {"status": expected_status, "response": response}
        return call

    def assert_request(self, verb, path, **expected):
        """Check the wire request for an operation."""
        call = getattr(self.http, verb)
        call.assert_called_once()
        args = call.call_args.kwargs
        self.assertEqual(self.root + path, args["url"])
        self.assertEqual("Bearer test-token", args["headers"]["Authorization"])
        for key, value in expected.items():
            self.assertEqual(value, args[key])

    def test_get_release_report(self):
        reports = {"results": [{"file_name": "report.csv"}]}
        self.check_request("get", "", reports)
        self.assertEqual(reports, self.report.get_release_report()["response"])
        self.assert_request("get", "", params=None)

    def test_create_release_report(self):
        body = {"begin_date": "2024-01-01", "end_date": "2024-01-31"}
        task = {"id": "task-1", "status": "pending"}
        self.check_request("post", "", task, 202)
        result = self.report.create_release_report(body)
        self.assertEqual((202, task), (result["status"], result["response"]))
        self.assert_request("post", "", data=json.dumps(body))

    def test_get_release_report_config(self):
        config = {"columns": ["date"]}
        self.check_request("get", "/config", config)
        self.assertEqual(config, self.report.get_release_report_config()["response"])
        self.assert_request("get", "/config")

    def test_create_release_report_config(self):
        config = {"columns": ["date"], "frequency": "daily"}
        self.check_request("post", "/config", config)
        self.assertEqual(config, self.report.create_release_report_config(config)["response"])
        self.assert_request("post", "/config", data=json.dumps(config))

    def test_update_release_report_config(self):
        config = {"columns": ["date"], "frequency": "weekly"}
        self.check_request("put", "/config", config)
        self.assertEqual(config, self.report.update_release_report_config(config)["response"])
        self.assert_request("put", "/config", data=json.dumps(config))

    def test_list_scheduled_release_reports(self):
        reports = {"results": [{"file_name": "scheduled.csv"}]}
        self.check_request("get", "/list", reports)
        self.assertEqual(reports, self.report.list_scheduled_release_reports()["response"])
        self.assert_request("get", "/list")

    def test_disable_release_report_schedule(self):
        self.check_request("delete", "/schedule", None)
        self.assertEqual(None, self.report.disable_release_report_schedule()["response"])
        self.assert_request("delete", "/schedule")

    def test_enable_release_report_schedule(self):
        self.check_request("post", "/schedule", None)
        self.assertEqual(None, self.report.enable_release_report_schedule()["response"])
        self.assert_request("post", "/schedule", data=None)

    def test_search_release_reports(self):
        filters = {"begin_date": "2024-01-01T00:00:00Z", "end_date": "2024-01-31T00:00:00Z"}
        reports = {"results": []}
        self.check_request("get", "/search", reports)
        self.assertEqual(reports, self.report.search_release_reports(filters)["response"])
        self.assert_request("get", "/search", params=filters)

    def test_get_release_report_task(self):
        task = {"id": "task/1", "status": "done"}
        self.check_request("get", "/task/task%2F1", task)
        self.assertEqual(task, self.report.get_release_report_task("task/1")["response"])
        self.assert_request("get", "/task/task%2F1")

    def test_download_release_report(self):
        payload = b"id,name\n1,caf\xc3\xa9\n"
        self.check_request("get", "/report%2F1.csv", payload)
        result = self.report.download_release_report("report/1.csv")
        self.assertEqual(payload, result["response"])
        self.assert_request("get", "/report%2F1.csv", response_format="bytes")

    def test_release_report_factory_options(self):
        options = RequestOptions(access_token="other-token")
        resource = self.sdk.release_report(options)
        self.assertIsInstance(resource, ReleaseReport)
        self.assertIs(options, resource.request_options)

    @patch("mercadopago.http.http_client.requests.Session")
    def test_download_transport_keeps_bytes_and_json_errors(self, session_factory):
        session = session_factory.return_value.__enter__.return_value
        response = session.request.return_value
        response.status_code = 200
        response.content = b"a,b\n1,\xff\n"
        transport = HttpClient()
        result = transport.get("https://api.mercadopago.com/report.csv", headers={
            "Authorization": "Bearer test-token"}, response_format="bytes")
        self.assertEqual(response.content, result["response"])
        self.assertEqual(200, result["status"])
        self.assertEqual("Bearer test-token", session.request.call_args.kwargs["headers"]["Authorization"])
        response.status_code = 404
        response.content = b'{"message":"not found"}'
        response.json.return_value = {"message": "not found"}
        self.assertEqual({"message": "not found"}, transport.get(
            "https://api.mercadopago.com/report.csv", headers={},
            response_format="bytes")["response"])
        response.status_code = 200
        response.json.return_value = {"results": []}
        self.assertEqual({"results": []}, transport.get(
            "https://api.mercadopago.com/report", headers={})["response"])
        response.json.side_effect = ValueError("invalid")
        with self.assertRaises(MPServerError):
            transport.get("https://api.mercadopago.com/report", headers={})


if __name__ == "__main__":
    unittest.main()