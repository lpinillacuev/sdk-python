"""Releases Report resource for the MercadoPago API.

Provides report generation, listing, and scheduled report configuration.
"""
from mercadopago.core import MPBase


class ReleasesReport(MPBase):
    """Manages releases reports for the authenticated account."""

    def search_release_reports(self, begin_date=None, end_date=None, request_options=None):
        """Searches releases reports within an optional date range.

        Args:
            begin_date: Optional start date-time query parameter.
            end_date: Optional end date-time query parameter.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Matching reports and HTTP status.
        """
        filters = {}
        if begin_date is not None:
            filters["begin_date"] = begin_date
        if end_date is not None:
            filters["end_date"] = end_date
        return self._get(uri="/v1/account/release_report/search",
                         filters=filters or None, request_options=request_options)

    def download_release_report(self, file_name, request_options=None):
        """Downloads a generated releases report as raw CSV bytes.

        Args:
            file_name: Name of the generated CSV file.
            request_options: Per-call configuration overrides.

        Returns:
            dict: CSV bytes and HTTP status, or a parsed error response.
        """
        return self._get_binary(
            uri="/v1/account/release_report/" + self._path_param(file_name),
            request_options=request_options,
        )

    def get_release_report_task(self, task_id, request_options=None):
        """Retrieves the status of a releases report generation task.

        Args:
            task_id: Identifier of the task to retrieve.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Task status and HTTP status.
        """
        return self._get(uri="/v1/account/release_report/task/" + self._path_param(task_id),
                         request_options=request_options)

    def update_release_report_config(self, report_config, request_options=None):
        """Updates the scheduled releases report configuration.

        Args:
            report_config: ReportConfig dict describing the report schedule.
            request_options: Per-call configuration overrides.

        Returns:
            dict: The updated configuration and HTTP status.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")
        return self._put(uri="/v1/account/release_report/config",
                         data=report_config, request_options=request_options)

    def list_scheduled_release_reports(self, request_options=None):
        """Lists scheduled releases reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: The scheduled reports and HTTP status.
        """
        return self._get(uri="/v1/account/release_report/list",
                         request_options=request_options)

    def disable_release_report_schedule(self, request_options=None):
        """Disables automatic releases report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: The result and HTTP status.
        """
        return self._delete(uri="/v1/account/release_report/schedule",
                            request_options=request_options)

    def enable_release_report_schedule(self, request_options=None):
        """Enables automatic releases report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: The result and HTTP status.
        """
        return self._post(uri="/v1/account/release_report/schedule",
                          request_options=request_options)

    def get_release_report(self, request_options=None):
        """Retrieves the releases report list.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: The releases report list and HTTP status.
        """
        return self._get(uri="/v1/account/release_report",
                         request_options=request_options)

    def create_release_report(self, report_request, request_options=None):
        """Starts generation of a one-time releases report.

        Args:
            report_request: ReportRequest dict with begin_date and end_date.
            request_options: Per-call configuration overrides.

        Returns:
            dict: The report task and HTTP status.

        Raises:
            ValueError: If report_request is not a dict.
        """
        if not isinstance(report_request, dict):
            raise ValueError("Param report_request must be a Dictionary")

        return self._post(uri="/v1/account/release_report", data=report_request,
                          request_options=request_options)

    def get_release_report_config(self, request_options=None):
        """Retrieves the releases report configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: The current report configuration and HTTP status.
        """
        return self._get(uri="/v1/account/release_report/config",
                         request_options=request_options)

    def create_release_report_config(self, report_config, request_options=None):
        """Creates a scheduled releases report configuration.

        Args:
            report_config: ReportConfig dict describing the report schedule.
            request_options: Per-call configuration overrides.

        Returns:
            dict: The created report configuration and HTTP status.

        Raises:
            ValueError: If report_config is not a dict.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")

        return self._post(uri="/v1/account/release_report/config",
                          data=report_config, request_options=request_options)