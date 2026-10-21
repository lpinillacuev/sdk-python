"""Claims resource for the MercadoPago post-purchase API."""
from mercadopago.core import MPBase


class Claims(MPBase):
    """Retrieves claims and submits shipping evidence."""

    def request_claim_mediation(self, claim_id, request_options=None):
        """Requests mediation for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Mediation request response.
        """
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/open-dispute",
            request_options=request_options,
        )

    def send_claim_message(self, claim_id, message_object, application_id=None,
                           request_options=None):
        """Sends a message in a claim thread.

        Args:
            claim_id: Identifier of the claim.
            message_object: Dict containing message and optional attachments.
            application_id: Optional application identifier in the query string.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Message submission response.
        """
        if not isinstance(message_object, dict):
            raise ValueError("Param message_object must be a Dictionary")

        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/send-message",
            data=message_object,
            params={"application_id": application_id} if application_id is not None else None,
            request_options=request_options,
        )

    def download_claim_file(self, claim_id, file_name, request_options=None):
        """Downloads an attachment as raw bytes.

        Args:
            claim_id: Identifier of the claim.
            file_name: Name of the attachment.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Download response with raw bytes in ``response``.
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
            file_name: Name of the attachment.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Attachment metadata response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name),
            request_options=request_options,
        )

    def attach_claim_file(self, claim_id, file, request_options=None):
        """Attaches a file to a claim.

        Args:
            claim_id: Identifier of the claim.
            file: JPEG, PNG, or PDF file to attach (up to 10 MB).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Attachment upload response.
        """
        return self._post_multipart(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments",
            files={"file": file},
            request_options=request_options,
        )

    def get_claim_evidence(self, claim_id, request_options=None):
        """Lists evidence submitted for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim evidence list response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/evidences",
            request_options=request_options,
        )

    def get_claim_reasons(self, reason_id, request_options=None):
        """Retrieves a claim reason by its identifier.

        Args:
            reason_id: Identifier of the claim reason.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim reason response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/reasons/" + self._path_param(reason_id),
            request_options=request_options,
        )

    def search_claims(self, filters=None, request_options=None):
        """Searches claims with optional query parameters.

        Args:
            filters: Query parameters (id, type, stage, status, limit, offset).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated claims search results.
        """
        return self._get(
            uri="/post-purchase/v1/claims/search",
            filters=filters,
            request_options=request_options,
        )

    def get_claim(self, claim_id, request_options=None):
        """Retrieves a claim by its identifier.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim details.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id),
            request_options=request_options,
        )

    def get_claim_mediation_resolutions(self, claim_id, request_options=None):
        """Retrieves the expected mediation resolutions for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Expected mediation resolutions response.
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
            dict: Claim message thread response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/messages",
            request_options=request_options,
        )

    def get_claim_history(self, claim_id, request_options=None):
        """Retrieves the status history for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim status history response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/status_history",
            request_options=request_options,
        )

    def upload_shipping_evidence(self, claim_id, evidence_object, request_options=None):
        """Uploads JSON shipping evidence for a claim.

        Args:
            claim_id: Identifier of the claim.
            evidence_object: Dict containing type and value.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Upload response.
        """
        if not isinstance(evidence_object, dict):
            raise ValueError("Param evidence_object must be a Dictionary")

        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/evidences",
            data=evidence_object,
            request_options=request_options,
        )