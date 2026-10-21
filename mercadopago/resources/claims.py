"""Claims resource for post-purchase claim and evidence operations."""
from mercadopago.core import MPBase


class Claims(MPBase):
    """Provides access to post-purchase claims."""

    def request_claim_mediation(self, claim_id, request_options=None):
        """Requests mediation for a claim.

        Args:
            claim_id: Claim identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Mediation request response.
        """
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/open-dispute", request_options=request_options,
        )

    def send_claim_message(self, claim_id, data, application_id=None,
                           request_options=None):
        """Sends a message in a claim thread.

        Args:
            claim_id: Claim identifier.
            data: Message body containing message and optional attachments.
            application_id: Optional application identifier query parameter.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Sent message response.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")
        params = {"application_id": application_id} if application_id is not None else None
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/send-message", data=data, params=params,
            request_options=request_options,
        )

    def attach_claim_file(self, claim_id, file, request_options=None):
        """Attaches a file to a claim.

        Args:
            claim_id: Claim identifier.
            file: JPEG, PNG, or PDF file to attach (maximum 10 MB).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Attached file metadata response.
        """
        return self._post_multipart(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments", files={"file": file},
            request_options=request_options,
        )

    def get_claim_file(self, claim_id, file_name, request_options=None):
        """Retrieves JSON metadata for a file attached to a claim.

        Args:
            claim_id: Claim identifier.
            file_name: Attached file name.
            request_options: Per-call configuration overrides.

        Returns:
            dict: File metadata response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name),
            request_options=request_options,
        )

    def download_claim_file(self, claim_id, file_name, request_options=None):
        """Downloads an attached claim file as raw bytes.

        Args:
            claim_id: Claim identifier.
            file_name: Attached file name.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and binary file content.
        """
        return self._get_binary(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name) + "/download",
            request_options=request_options,
        )

    def get_claim_evidence(self, claim_id, request_options=None):
        """Retrieves evidence for a claim.

        Args:
            claim_id: Claim identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim evidence list response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/evidences", request_options=request_options,
        )

    def get_claim_reasons(self, reason_id, request_options=None):
        """Retrieves a claim reason by ID.

        Args:
            reason_id: Claim reason identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim reason response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/reasons/" + self._path_param(reason_id),
            request_options=request_options,
        )

    def search_claims(self, filters=None, request_options=None):
        """Searches claims using query filters.

        Args:
            filters: Optional query parameters including id, type, stage,
                status, limit, and offset.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Matching claims and pagination details.
        """
        if filters is not None and not isinstance(filters, dict):
            raise ValueError("Param filters must be a Dictionary")
        return self._get(
            uri="/post-purchase/v1/claims/search", filters=filters,
            request_options=request_options,
        )

    def get_claim(self, claim_id, request_options=None):
        """Retrieves a claim by ID.

        Args:
            claim_id: Claim identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim details.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id),
            request_options=request_options,
        )

    def get_claim_mediation_resolutions(self, claim_id, request_options=None):
        """Retrieves expected mediation resolutions for a claim.

        Args:
            claim_id: Claim identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Expected mediation resolutions response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/expected-resolutions", request_options=request_options,
        )

    def get_claim_messages(self, claim_id, request_options=None):
        """Retrieves the message thread for a claim.

        Args:
            claim_id: Claim identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim messages response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/messages", request_options=request_options,
        )

    def get_claim_history(self, claim_id, request_options=None):
        """Retrieves status history for a claim.

        Args:
            claim_id: Claim identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim status history response.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/status_history", request_options=request_options,
        )

    def upload_shipping_evidence(self, claim_id, data, request_options=None):
        """Uploads shipping evidence for a claim.

        Args:
            claim_id: Claim identifier.
            data: Evidence with type and value fields.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Upload response.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/evidences", data=data, request_options=request_options,
        )