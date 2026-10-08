"""Post-purchase claim, message, resolution, and shipping operations."""
from mercadopago.core import MPBase


class Claim(MPBase):
    """Client for the post-purchase Claims APIs."""

    _BASE_URI = "/post-purchase/v1/claims"

    def get(self, claim_id, request_options=None):
        return self._get(
            f"{self._BASE_URI}/{self._path_param(claim_id)}",
            request_options=request_options,
        )

    def search(self, filters=None, request_options=None):
        return self._get(
            f"{self._BASE_URI}/search",
            filters=filters,
            request_options=request_options,
        )

    def get_reason(self, reason_id, request_options=None):
        return self._get(
            f"{self._BASE_URI}/reasons/{self._path_param(reason_id)}",
            request_options=request_options,
        )

    def get_history(self, claim_id, request_options=None):
        return self._get(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/status_history",
            request_options=request_options,
        )

    def get_evidence(self, claim_id, request_options=None):
        return self._get(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/evidences",
            request_options=request_options,
        )

    def get_messages(self, claim_id, request_options=None):
        return self._get(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/messages",
            request_options=request_options,
        )

    def send_message(self, claim_id, data, application_id=None,
                     request_options=None):
        params = None
        if application_id is not None:
            params = {"application_id": application_id}
        return self._post(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/actions/send-message",
            data=data,
            params=params,
            request_options=request_options,
        )

    def attach_file(self, claim_id, file, request_options=None):
        return self._post_multipart(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/attachments",
            files={"file": file},
            request_options=request_options,
        )

    def get_file(self, claim_id, file_name, request_options=None):
        return self._get(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/attachments/"
            f"{self._path_param(file_name)}",
            request_options=request_options,
        )

    def download_file(self, claim_id, file_name, request_options=None):
        return self._get_binary(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/attachments/"
            f"{self._path_param(file_name)}/download",
            request_options=request_options,
        )

    def request_mediation(self, claim_id, request_options=None):
        return self._post(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/actions/open-dispute",
            request_options=request_options,
        )

    def get_mediation_resolutions(self, claim_id, request_options=None):
        return self._get(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/expected-resolutions",
            request_options=request_options,
        )

    def upload_shipping_evidence(self, claim_id, data, request_options=None):
        return self._post(
            f"{self._BASE_URI}/{self._path_param(claim_id)}/actions/evidences",
            data=data,
            request_options=request_options,
        )