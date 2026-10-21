"""Claims resource for the Mercado Pago post-purchase API."""
from mercadopago.core import MPBase


class Claims(MPBase):
    def attach_claim_file(self, claim_id, file, request_options=None):
        """Attaches a JPEG, PNG, or PDF file (up to 10 MB) to a claim.

        Args:
            claim_id: Identifier of the claim.
            file: Binary file to attach.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Attached file details and response status.
        """
        return self._post_multipart(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments",
            files={"file": file},
            request_options=request_options,
        )

    """Retrieves claims, reasons, and attachment metadata."""

    def get_claim_reasons(self, reason_id, request_options=None):
        """Retrieves a claim reason by ID.

        Args:
            reason_id: Identifier of the reason.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim reason details and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/reasons/" + self._path_param(reason_id),
            request_options=request_options,
        )

    def search_claims(self, filters=None, request_options=None):
        """Searches claims using query filters.

        Args:
            filters: Query parameters such as ``id``, ``type``, ``stage``,
                ``status``, ``limit``, and ``offset``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Search results and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/search",
            filters=filters,
            request_options=request_options,
        )

    def get_claim(self, claim_id, request_options=None):
        """Retrieves a claim by ID.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim details and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id),
            request_options=request_options,
        )

    def get_claim_evidence(self, claim_id, request_options=None):
        """Retrieves evidence for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Evidence list and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/evidences",
            request_options=request_options,
        )

    def get_claim_mediation_resolutions(self, claim_id, request_options=None):
        """Retrieves expected mediation resolutions for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Resolution options and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/expected-resolutions",
            request_options=request_options,
        )

    def get_claim_messages(self, claim_id, request_options=None):
        """Retrieves the message thread for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Message thread and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/messages",
            request_options=request_options,
        )

    def get_claim_history(self, claim_id, request_options=None):
        """Retrieves status history for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: History entries and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/status_history",
            request_options=request_options,
        )

    def upload_shipping_evidence(self, claim_id, data, request_options=None):
        """Uploads shipping evidence to support a claim.

        Args:
            claim_id: Identifier of the claim.
            data: Evidence with ``type`` and ``value`` fields.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Upload response and status.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/evidences",
            data=data,
            request_options=request_options,
        )

    def request_claim_mediation(self, claim_id, request_options=None):
        """Requests mediation for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Mediation response and status.
        """
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/open-dispute",
            request_options=request_options,
        )

    def send_claim_message(self, claim_id, data, application_id=None,
                           request_options=None):
        """Sends a message in a claim thread.

        Args:
            claim_id: Identifier of the claim.
            data: Message request with ``message`` and optional ``attachments``.
            application_id: Optional application ID query parameter.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Message response and status.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/send-message",
            data=data,
            params={"application_id": application_id} if application_id is not None else None,
            request_options=request_options,
        )

    def download_claim_file(self, claim_id, file_name, request_options=None):
        """Downloads the binary content of a claim attachment.

        Args:
            claim_id: Identifier of the claim.
            file_name: Attachment name (``fileName`` in the API path).
            request_options: Per-call configuration overrides.

        Returns:
            dict: File bytes and response status.
        """
        return self._get_binary(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name) + "/download",
            request_options=request_options,
        )

    def get_claim_file(self, claim_id, file_name, request_options=None):
        """Retrieves metadata for a claim attachment.

        Args:
            claim_id: Identifier of the claim.
            file_name: Attachment name (``fileName`` in the API path).
            request_options: Per-call configuration overrides.

        Returns:
            dict: File metadata and response status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name),
            request_options=request_options,
        )