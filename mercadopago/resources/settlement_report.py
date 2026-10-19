"""Settlement report operations for the Mercado Pago account API.

JSON endpoints use the standard MPBase helpers. Downloading a report is a
binary response and is handled by the report transport instead of JSON parsing.
"""
from mercadopago.core import MPBase


class SettlementReport(MPBase):
    """Manage settlement report configuration, tasks and generated files."""

    _URI = "/v1/account/settlement_report"

    def get_settlement_report(self, request_options=None):
        """List settlement reports (ReportListResult)."""
        return self._get(uri=self._URI, request_options=request_options)

    def create_settlement_report(self, data, request_options=None):
        """Start a one-time report with a JSON ReportRequest."""
        return self._post(uri=self._URI, data=data, request_options=request_options)

    def get_settlement_report_config(self, request_options=None):
        """Get the scheduled report configuration (ReportConfig)."""
        return self._get(uri=self._URI + "/config", request_options=request_options)

    def create_settlement_report_config(self, data, request_options=None):
        """Create a ReportConfig using a JSON body."""
        return self._post(uri=self._URI + "/config", data=data,
                          request_options=request_options)

    def update_settlement_report_config(self, data, request_options=None):
        """Update the ReportConfig using a JSON body."""
        return self._put(uri=self._URI + "/config", data=data,
                         request_options=request_options)

    def list_scheduled_settlement_reports(self, request_options=None):
        """List scheduled reports (ReportListResult)."""
        return self._get(uri=self._URI + "/list", request_options=request_options)

    def disable_settlement_report_schedule(self, request_options=None):
        """Disable automatic report generation."""
        return self._delete(uri=self._URI + "/schedule", request_options=request_options)

    def enable_settlement_report_schedule(self, request_options=None):
        """Enable automatic report generation."""
        return self._post(uri=self._URI + "/schedule", request_options=request_options)

    def search_settlement_reports(self, begin_date=None, end_date=None,
                                  request_options=None):
        """Search reports by begin_date and end_date query parameters."""
        filters = {}
        if begin_date is not None:
            filters["begin_date"] = begin_date
        if end_date is not None:
            filters["end_date"] = end_date
        return self._get(uri=self._URI + "/search", filters=filters,
                         request_options=request_options)

    def get_settlement_report_task(self, task_id, request_options=None):
        """Get a report task by its escaped identifier (ReportTask)."""
        return self._get(uri=self._URI + "/task/" + self._path_param(task_id),
                         request_options=request_options)

    def download_settlement_report(self, file_name, request_options=None):
        """Download a CSV report as bytes using the binary report transport."""
        return self._get_binary(uri=self._URI + "/" + self._path_param(file_name),
                                request_options=request_options)