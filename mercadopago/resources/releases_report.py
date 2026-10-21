"""Releases report resource for the MercadoPago API."""
from mercadopago.core import MPBase


class ReleasesReport(MPBase):
    """Provides access to releases reports and their configuration."""

    def search_release_reports(self, filters=None, request_options=None):
        """Searches releases reports by date range.

        Args:
            filters: Optional query parameters, including begin_date and end_date.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Matching releases reports response.
        """
        if filters is not None and not isinstance(filters, dict):
            raise ValueError("Param filters must be a Dictionary")

        return self._get(
            uri="/v1/account/release_report/search",
            filters=filters,
            request_options=request_options,
        )

    def get_release_report_task(self, task_id, request_options=None):
        """Retrieves the status of a releases report generation task.

        Args:
            task_id: Identifier of the report generation task.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Report generation task status response.
        """
        return self._get(
            uri=f"/v1/account/release_report/task/{self._path_param(task_id)}",
            request_options=request_options,
        )

    def update_release_report_config(self, data, request_options=None):
        """Updates the releases report configuration.

        Args:
            data: ReportConfig dictionary for the automatic report.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated report configuration response.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._put(
            uri="/v1/account/release_report/config",
            data=data,
            request_options=request_options,
        )

    def list_scheduled_release_reports(self, request_options=None):
        """Lists scheduled releases reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Scheduled report list response.
        """
        return self._get(
            uri="/v1/account/release_report/list",
            request_options=request_options,
        )

    def disable_release_report_schedule(self, request_options=None):
        """Disables automatic releases report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Schedule disable response.
        """
        return self._delete(
            uri="/v1/account/release_report/schedule",
            request_options=request_options,
        )

    def enable_release_report_schedule(self, request_options=None):
        """Enables automatic releases report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Schedule enable response.
        """
        return self._post(
            uri="/v1/account/release_report/schedule",
            request_options=request_options,
        )

    """Provides access to releases reports and their configuration."""

    def get_release_report(self, request_options=None):
        """Lists releases reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Report list response.
        """
        return self._get(
            uri="/v1/account/release_report",
            request_options=request_options,
        )

    def create_release_report(self, data, request_options=None):
        """Generates a releases report for a date range.

        Args:
            data: ReportRequest dictionary containing the report date range.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Report generation task response.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._post(
            uri="/v1/account/release_report",
            data=data,
            request_options=request_options,
        )

    def get_release_report_config(self, request_options=None):
        """Retrieves the releases report configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Current report configuration response.
        """
        return self._get(
            uri="/v1/account/release_report/config",
            request_options=request_options,
        )

    def download_release_report(self, file_name, request_options=None):
        """Downloads a generated releases report as raw CSV bytes.

        Args:
            file_name: Name of the report file to download.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Download response with CSV bytes in ``response``.
        """
        return self._get_binary(
            uri=f"/v1/account/release_report/{self._path_param(file_name)}",
            request_options=request_options,
        )

    def create_release_report_config(self, data, request_options=None):
        """Creates the automatic releases report configuration.

        Args:
            data: ReportConfig dictionary for the automatic report.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created report configuration response.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._post(
            uri="/v1/account/release_report/config",
            data=data,
            request_options=request_options,
        )