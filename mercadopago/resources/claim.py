"""Post-purchase claim resource for the Mercado Pago API."""

from mercadopago.core import MPBase


class Claim(MPBase):
    """Access claims, evidence, messages, resolutions and attachments."""

    _ROOT = "/post-purchase/v1/claims"

    def get_reasons(self, reason_id, request_options=None):
        """Retrieve one claim reason as JSON."""
        return self._get(
            uri=f"{self._ROOT}/reasons/{self._path_param(reason_id)}",
            request_options=request_options,
        )

    def search(self, filters=None, request_options=None):
        """Search claims using id, type, stage, status, limit and offset filters."""
        return self._get(
            uri=self._ROOT + "/search", filters=filters,
            request_options=request_options,
        )

    def get(self, claim_id, request_options=None):
        """Retrieve a claim as JSON."""
        return self._get(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}",
            request_options=request_options,
        )

    def upload_shipping_evidence(self, claim_id, evidence, request_options=None):
        """Submit shipping evidence with type and value as JSON."""
        return self._post(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/actions/evidences",
            data=evidence, request_options=request_options,
        )

    def request_mediation(self, claim_id, request_options=None):
        """Request mediation without a required request body."""
        return self._post(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/actions/open-dispute",
            request_options=request_options,
        )

    def send_message(self, claim_id, message, application_id=None, request_options=None):
        """Send a JSON message, optionally scoped to an application."""
        params = {"application_id": application_id} if application_id is not None else None
        return self._post(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/actions/send-message",
            data=message, params=params, request_options=request_options,
        )

    def attach_file(self, claim_id, file, request_options=None):
        """Attach a binary file using a multipart form field named file."""
        # File uploads require a multipart-aware transport helper, not the
        # JSON-encoding _post helper.
        return self._post_multipart(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/attachments",
            files={"file": file}, request_options=request_options,
        )

    def get_file(self, claim_id, file_name, request_options=None):
        """Retrieve JSON metadata for an attached file (not its content)."""
        return self._get(
            uri=(f"{self._ROOT}/{self._path_param(claim_id)}/attachments/"
                 f"{self._path_param(file_name)}"),
            request_options=request_options,
        )

    def download_file(self, claim_id, file_name, request_options=None):
        """Download an attached file as raw bytes."""
        return self._get_binary(
            uri=(f"{self._ROOT}/{self._path_param(claim_id)}/attachments/"
                 f"{self._path_param(file_name)}/download"),
            request_options=request_options,
        )

    def get_evidence(self, claim_id, request_options=None):
        """List the evidence for a claim as JSON."""
        return self._get(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/evidences",
            request_options=request_options,
        )

    def get_mediation_resolutions(self, claim_id, request_options=None):
        """List expected mediation resolutions as JSON."""
        return self._get(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/expected-resolutions",
            request_options=request_options,
        )

    def get_messages(self, claim_id, request_options=None):
        """List messages in the claim thread as JSON."""
        return self._get(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/messages",
            request_options=request_options,
        )

    def get_history(self, claim_id, request_options=None):
        """List the status history of a claim as JSON."""
        return self._get(
            uri=f"{self._ROOT}/{self._path_param(claim_id)}/status_history",
            request_options=request_options,
        )