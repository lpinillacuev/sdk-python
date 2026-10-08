"""Wire-level tests for releases and settlements report resources."""
import unittest

from tests.base_client_test import BaseClientTest


class ReportContractMixin:
    """Exercise the common ten-operation report contract."""

    factory = None
    report_name = None

    def resource(self):
        return getattr(self.sdk, self.factory)()

    def path(self, suffix=""):
        return f"/v1/account/{self.report_name}{suffix}"

    def test_config_operations(self):
        data = {"file_name_prefix": "report"}
        self.mock_post({}, status=200)
        self.resource().create_config(data)
        self.assert_http_call("post", self.path("/config"), data='{"file_name_prefix": "report"}')

        self.mock_put({})
        self.resource().update_config(data)
        self.assert_http_call("put", self.path("/config"), data='{"file_name_prefix": "report"}')

        self.mock_get({})
        self.resource().get_config()
        self.assert_http_call("get", self.path("/config"))

    def test_generation_listing_and_search(self):
        data = {"begin_date": "2024-01-01", "end_date": "2024-01-31"}
        self.mock_post({}, status=202)
        self.resource().create(data)
        self.assert_http_call("post", self.path(), data=('{' + '"begin_date": "2024-01-01", '
                                                          '"end_date": "2024-01-31"}'))

        self.mock_get({})
        self.resource().list()
        self.assert_http_call("get", self.path())

        filters = {"begin_date": "2024-01-01", "end_date": "2024-01-31"}
        self.mock_get({})
        self.resource().search(filters)
        self.assert_http_call("get", self.path("/search"), params=filters)

    def test_task_schedule_scheduled_list_and_download(self):
        self.mock_get({})
        self.resource().get_task("task/1")
        self.assert_http_call("get", self.path("/task/task%2F1"))

        self.mock_post({}, status=200)
        self.resource().enable_schedule()
        self.assert_http_call("post", self.path("/schedule"))

        self.mock_delete({}, status=200)
        self.resource().disable_schedule()
        self.assert_http_call("delete", self.path("/schedule"))

        self.mock_get({})
        self.resource().list_scheduled()
        self.assert_http_call("get", self.path("/list"))

        self.mock_get_bytes(b"a,b\n1,2\n")
        result = self.resource().download("report/1.csv")
        self.assertEqual(b"a,b\n1,2\n", result["response"])
        self.assert_http_call("get", self.path("/report%2F1.csv"))


class TestReleaseReport(ReportContractMixin, BaseClientTest):
    factory = "release_report"
    report_name = "release_report"


class TestSettlementReport(ReportContractMixin, BaseClientTest):
    factory = "settlement_report"
    report_name = "settlement_report"


if __name__ == "__main__":
    unittest.main()