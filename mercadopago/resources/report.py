"""Releases and settlements report resources."""
from mercadopago.core import MPBase


class _Report(MPBase):
    """Shared operations for account report APIs."""

    report_name = None

    @property
    def base_uri(self):
        return f"/v1/account/{self.report_name}"

    def create_config(self, data, request_options=None):
        return self._post(f"{self.base_uri}/config", data, request_options=request_options)

    def update_config(self, data, request_options=None):
        return self._put(f"{self.base_uri}/config", data, request_options=request_options)

    def get_config(self, request_options=None):
        return self._get(f"{self.base_uri}/config", request_options=request_options)

    def create(self, data, request_options=None):
        return self._post(self.base_uri, data, request_options=request_options)

    def list(self, request_options=None):
        return self._get(self.base_uri, request_options=request_options)

    def search(self, filters=None, request_options=None):
        return self._get(f"{self.base_uri}/search", filters, request_options)

    def get_task(self, task_id, request_options=None):
        return self._get(
            f"{self.base_uri}/task/{self._path_param(task_id)}",
            request_options=request_options,
        )

    def enable_schedule(self, request_options=None):
        return self._post(f"{self.base_uri}/schedule", request_options=request_options)

    def disable_schedule(self, request_options=None):
        return self._delete(f"{self.base_uri}/schedule", request_options=request_options)

    def list_scheduled(self, request_options=None):
        return self._get(f"{self.base_uri}/list", request_options=request_options)

    def download(self, file_name, request_options=None):
        return self._get(
            f"{self.base_uri}/{self._path_param(file_name)}",
            request_options=request_options,
        )


class ReleaseReport(_Report):
    """Releases report API."""

    report_name = "release_report"


class SettlementReport(_Report):
    """Settlements report API."""

    report_name = "settlement_report"