"""Unit tests for the ReleasesReport resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestReleasesReport(BaseClientTest):
    """Test Module: ReleasesReport"""

    def test_get_release_report(self):
        self.mock_get({"results": []})

        result = self.sdk.releases_report().get_release_report()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_release_report(self):
        payload = {"begin_date": "2025-01-01", "end_date": "2025-01-31"}
        self.mock_post({"id": "task-1"})

        result = self.sdk.releases_report().create_release_report(payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_get_release_report_config(self):
        self.mock_get({"columns": []})

        result = self.sdk.releases_report().get_release_report_config()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/config",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_release_report_config(self):
        payload = {"columns": ["date", "amount"], "frequency": "monthly"}
        self.mock_post({"columns": payload["columns"]})

        result = self.sdk.releases_report().create_release_report_config(payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/config",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_update_release_report_config(self):
        payload = {"columns": [{"key": "DATE", "alias": "transaction_date"}],
                   "frequency": {"hour": 10, "type": "monthly"}}
        self.mock_put({"columns": payload["columns"]})

        result = self.sdk.releases_report().update_release_report_config(payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/config",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_list_scheduled_release_reports(self):
        self.mock_get({"results": []})

        result = self.sdk.releases_report().list_scheduled_release_reports()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/list",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_disable_release_report_schedule(self):
        self.mock_http.delete.return_value = {"status": 200, "response": None}

        result = self.sdk.releases_report().disable_release_report_schedule()

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/schedule",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_enable_release_report_schedule(self):
        self.mock_post(None)

        result = self.sdk.releases_report().enable_release_report_schedule()

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/schedule",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])


    def test_search_release_reports(self):
        filters = {"begin_date": "2025-01-01", "end_date": "2025-01-31"}
        self.mock_get({"results": []})

        result = self.sdk.releases_report().search_release_reports(filters)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/search",
            kwargs["url"],
        )
        self.assertEqual(filters, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_release_report_task(self):
        self.mock_get({"id": "task-1", "status": "done"})

        result = self.sdk.releases_report().get_release_report_task("task-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/task/task-1",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()