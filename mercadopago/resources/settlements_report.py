"""Settlements report resource for the MercadoPago API."""
from mercadopago.core import MPBase


class SettlementsReport(MPBase):
    """Manages settlements reports and their configuration."""

    def download_settlement_report(self, file_name, request_options=None):
        """Downloads a settlements report as CSV bytes.

        Args:
            file_name: Name of the report file to download.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and raw CSV bytes (or a parsed error).
        """
        return self._get_binary(
            uri="/v1/account/settlement_report/" + self._path_param(file_name),
            request_options=request_options,
        )

    def update_settlement_report_config(self, report_config, request_options=None):
        """Updates the settlements report configuration.

        Args:
            report_config: ReportConfig dict for scheduled report generation.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated report configuration.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")

        return self._put(uri="/v1/account/settlement_report/config",
                         data=report_config, request_options=request_options)

    def list_scheduled_settlement_reports(self, request_options=None):
        """Lists scheduled settlements reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Scheduled report list.
        """
        return self._get(uri="/v1/account/settlement_report/list",
                         request_options=request_options)

    def disable_settlement_report_schedule(self, request_options=None):
        """Disables automatic settlements report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Schedule disable response.
        """
        return self._delete(uri="/v1/account/settlement_report/schedule",
                            request_options=request_options)

    def enable_settlement_report_schedule(self, request_options=None):
        """Enables automatic settlements report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Schedule enable response.
        """
        return self._post(uri="/v1/account/settlement_report/schedule",
                          request_options=request_options)

    def get_settlement_report(self, request_options=None):
        """Lists settlements reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Available settlements reports.
        """
        return self._get(uri="/v1/account/settlement_report",
                         request_options=request_options)

    def create_settlement_report(self, report_request, request_options=None):
        """Starts generation of a settlements report.

        Args:
            report_request: ReportRequest dict describing the date range.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Report generation task.
        """
        if not isinstance(report_request, dict):
            raise ValueError("Param report_request must be a Dictionary")

        return self._post(uri="/v1/account/settlement_report",
                          data=report_request, request_options=request_options)

    def get_settlement_report_config(self, request_options=None):
        """Retrieves the settlements report configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Current report configuration.
        """
        return self._get(uri="/v1/account/settlement_report/config",
                         request_options=request_options)

    def search_settlement_reports(self, begin_date=None, end_date=None, request_options=None):
        """Searches settlements reports by optional date range.

        Args:
            begin_date: Optional start date-time of the search.
            end_date: Optional end date-time of the search.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Matching settlements reports.
        """
        filters = {}
        if begin_date is not None:
            filters["begin_date"] = begin_date
        if end_date is not None:
            filters["end_date"] = end_date
        return self._get(uri="/v1/account/settlement_report/search",
                         filters=filters, request_options=request_options)

    def get_settlement_report_task(self, task_id, request_options=None):
        """Retrieves a settlements report task by its ID.

        Args:
            task_id: Identifier of the report task.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Report task status.
        """
        return self._get(uri="/v1/account/settlement_report/task/" +
                         self._path_param(task_id), request_options=request_options)

    def create_settlement_report_config(self, report_config, request_options=None):
        """Creates a settlements report configuration.

        Args:
            report_config: ReportConfig dict for scheduled report generation.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created report configuration.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")

        return self._post(uri="/v1/account/settlement_report/config",
                          data=report_config, request_options=request_options)