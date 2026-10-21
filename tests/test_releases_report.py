"""Unit tests for the ReleasesReport resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestReleasesReport(BaseClientTest):
    """Test Module: ReleasesReport"""

    def test_search_release_reports(self):
        self.mock_get({"results": []})
        begin_date = "2024-01-01T00:00:00Z"
        end_date = "2024-01-31T23:59:59Z"

        result = self.sdk.releases_report().search_release_reports(begin_date, end_date)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/search",
                         kwargs["url"])
        self.assertEqual({"begin_date": begin_date, "end_date": end_date}, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_download_release_report(self):
        csv_bytes = b"date,amount\n2024-01-01,10.00\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": csv_bytes}
        file_name = "releases_report_2024-01-01_2024-01-31.csv"

        result = self.sdk.releases_report().download_release_report(file_name)

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/" + file_name,
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(csv_bytes, result["response"])

    def test_get_release_report_task(self):
        self.mock_get({"id": "task-1", "status": "done"})

        result = self.sdk.releases_report().get_release_report_task("task-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/task/task-1",
                         kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_release_report(self):
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        result = self.sdk.releases_report().get_release_report()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_release_report(self):
        report_request = {"begin_date": "2024-01-01", "end_date": "2024-01-31"}
        self.mock_http.post.return_value = {"status": 202, "response": {"id": "1"}}

        result = self.sdk.releases_report().create_release_report(report_request)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report",
                         kwargs["url"])
        self.assertEqual(report_request, json.loads(kwargs["data"]))
        self.assertEqual(202, result["status"])

    def test_get_release_report_config(self):
        self.mock_http.get.return_value = {"status": 200, "response": {"id": "1"}}

        result = self.sdk.releases_report().get_release_report_config()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/config",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_release_report_config(self):
        report_config = {"columns": ["date", "amount"], "frequency": "daily"}
        self.mock_http.post.return_value = {"status": 200, "response": report_config}

        result = self.sdk.releases_report().create_release_report_config(report_config)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/config",
                         kwargs["url"])
        self.assertEqual(report_config, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_update_release_report_config(self):
        report_config = {"file_name_prefix": "releases_report", "frequency": {"type": "daily", "hour": 12}}
        self.mock_http.put.return_value = {"status": 200, "response": report_config}

        result = self.sdk.releases_report().update_release_report_config(report_config)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/config",
                         kwargs["url"])
        self.assertEqual(report_config, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_list_scheduled_release_reports(self):
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        result = self.sdk.releases_report().list_scheduled_release_reports()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/list",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_disable_release_report_schedule(self):
        self.mock_http.delete.return_value = {"status": 200, "response": None}

        result = self.sdk.releases_report().disable_release_report_schedule()

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/schedule",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_enable_release_report_schedule(self):
        self.mock_http.post.return_value = {"status": 200, "response": None}

        result = self.sdk.releases_report().enable_release_report_schedule()

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/schedule",
                         kwargs["url"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()