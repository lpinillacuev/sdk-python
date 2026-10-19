"""Releases report operations for the authenticated account."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from mercadopago.config.defaults import DEFAULT_RETRY_ON
from mercadopago.config.request_options import RequestOptions
from mercadopago.core import MPBase
from mercadopago.errors.exceptions import MPServerError
from mercadopago.errors.response import MPResponse


class ReleaseReport(MPBase):
    """Generate, configure, list and download releases reports."""

    def get_release_report(self, request_options=None):
        """List releases reports."""
        return self._get("/v1/account/release_report", request_options=request_options)

    def create_release_report(self, data, request_options=None):
        """Start generating a report from a JSON ReportRequest."""
        return self._post("/v1/account/release_report", data=data,
                          request_options=request_options)

    def get_release_report_config(self, request_options=None):
        """Retrieve the current report configuration."""
        return self._get("/v1/account/release_report/config",
                         request_options=request_options)

    def create_release_report_config(self, data, request_options=None):
        """Create a report configuration."""
        return self._post("/v1/account/release_report/config", data=data,
                          request_options=request_options)

    def update_release_report_config(self, data, request_options=None):
        """Update a report configuration."""
        return self._put("/v1/account/release_report/config", data=data,
                         request_options=request_options)

    def list_scheduled_release_reports(self, request_options=None):
        """List scheduled releases reports."""
        return self._get("/v1/account/release_report/list",
                         request_options=request_options)

    def disable_release_report_schedule(self, request_options=None):
        """Disable automatic report generation."""
        return self._delete("/v1/account/release_report/schedule",
                            request_options=request_options)

    def enable_release_report_schedule(self, request_options=None):
        """Enable automatic report generation without a request body."""
        return self._post("/v1/account/release_report/schedule",
                          request_options=request_options)

    def search_release_reports(self, begin_date=None, end_date=None,
                               request_options=None):
        """Search reports by optional begin_date and end_date query dates."""
        filters = {}
        if begin_date is not None:
            filters["begin_date"] = begin_date
        if end_date is not None:
            filters["end_date"] = end_date
        return self._get("/v1/account/release_report/search", filters=filters,
                         request_options=request_options)

    def get_release_report_task(self, task_id, request_options=None):
        """Retrieve the status of a report task by its escaped ID."""
        return self._get("/v1/account/release_report/task/" + self._path_param(task_id),
                         request_options=request_options)

    def download_release_report(self, file_name, request_options=None):
        """Download CSV bytes; error responses retain their JSON representation.

        The JSON-only HTTP client cannot decode binary content, so this call
        uses a session with the same authenticated headers and retry settings.
        """
        if request_options is not None and not isinstance(request_options, RequestOptions):
            raise ValueError("Param request_options must be a RequestOptions Object")
        options = request_options or self.request_options
        if options.access_token is None:
            options.access_token = self.request_options.access_token
        headers = options.get_headers()
        headers["Accept"] = "text/csv"
        retry_strategy = Retry(
            total=options.max_retries,
            status_forcelist=options.retry_on if options.retry_on is not None
            else DEFAULT_RETRY_ON,
        )
        url = (self.config.api_base_url + "/v1/account/release_report/"
               + self._path_param(file_name))
        with requests.Session() as session:
            session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
            result = session.request("GET", url, headers=headers,
                                     timeout=options.connection_timeout)
            response = {"status": result.status_code, "response": None}
            if result.content:
                if 200 <= result.status_code < 300:
                    response["response"] = result.content
                else:
                    try:
                        response["response"] = result.json()
                    except ValueError as exc:
                        raise MPServerError(
                            result.status_code,
                            {"message": "Invalid JSON in response body",
                             "error": "invalid_response"},
                        ) from exc
        return MPResponse(response)