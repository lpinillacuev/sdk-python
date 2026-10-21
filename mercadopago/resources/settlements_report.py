"""Settlements report resource for listing, generating, and configuring reports."""
from mercadopago.core import MPBase


class SettlementsReport(MPBase):
    """Provides access to settlement reports and their configuration."""

    def search_settlement_reports(self, filters=None, request_options=None):
        """Searches settlements reports by date range.

        Args:
            filters: Optional query dict with ``begin_date`` and ``end_date``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and matching settlements reports.
        """
        if filters is not None and not isinstance(filters, dict):
            raise ValueError("Param filters must be a Dictionary")

        return self._get(
            uri="/v1/account/settlement_report/search",
            filters=filters,
            request_options=request_options,
        )

    def download_settlement_report(self, file_name, request_options=None):
        """Downloads a settlements report as CSV bytes.

        Args:
            file_name: Name of the report file to download.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and raw CSV bytes.
        """
        return self._get_binary(
            uri=f"/v1/account/settlement_report/{self._path_param(file_name)}",
            request_options=request_options,
        )

    def get_settlement_report_task(self, task_id, request_options=None):
        """Retrieves the status of a settlements report task.

        Args:
            task_id: Identifier of the report generation task.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report task.
        """
        return self._get(
            uri=f"/v1/account/settlement_report/task/{self._path_param(task_id)}",
            request_options=request_options,
        )

    def update_settlement_report_config(self, data, request_options=None):
        """Updates the settlements report configuration.

        Args:
            data: ReportConfig dict defining the report configuration.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the updated report configuration.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._put(
            uri="/v1/account/settlement_report/config",
            data=data,
            request_options=request_options,
        )

    def list_scheduled_settlement_reports(self, request_options=None):
        """Lists scheduled settlements reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the scheduled report list.
        """
        return self._get(
            uri="/v1/account/settlement_report/list",
            request_options=request_options,
        )

    def disable_settlement_report_schedule(self, request_options=None):
        """Disables automatic settlements report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the API response.
        """
        return self._delete(
            uri="/v1/account/settlement_report/schedule",
            request_options=request_options,
        )

    def enable_settlement_report_schedule(self, request_options=None):
        """Enables automatic settlements report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the API response.
        """
        return self._post(
            uri="/v1/account/settlement_report/schedule",
            request_options=request_options,
        )

    def get_settlement_report(self, request_options=None):
        """Retrieves the available settlements reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the list of settlements reports.
        """
        return self._get(
            uri="/v1/account/settlement_report",
            request_options=request_options,
        )

    def create_settlement_report(self, data, request_options=None):
        """Starts generation of a report for a date range.

        Args:
            data: ReportRequest dict containing ``begin_date`` and ``end_date``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report generation task.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._post(
            uri="/v1/account/settlement_report",
            data=data,
            request_options=request_options,
        )

    def get_settlement_report_config(self, request_options=None):
        """Retrieves the current settlements report configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report configuration.
        """
        return self._get(
            uri="/v1/account/settlement_report/config",
            request_options=request_options,
        )

    def create_settlement_report_config(self, data, request_options=None):
        """Creates a scheduled settlements report configuration.

        Args:
            data: ReportConfig dict defining columns, frequency, and delivery.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the created report configuration.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._post(
            uri="/v1/account/settlement_report/config",
            data=data,
            request_options=request_options,
        )