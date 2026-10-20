"""Claims resource for the MercadoPago post-purchase API."""
from mercadopago.core import MPBase


class Claims(MPBase):
    """Manages files attached to post-purchase claims."""

    def attach_claim_file(self, claim_id, file, request_options=None):
        """Attach a JPEG, PNG, or PDF file to a claim.

        Args:
            claim_id: Identifier of the claim.
            file: File to upload as the required multipart ``file`` field.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Attachment details, including file_id and file_name.
        """
        return self._post_multipart(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id) + "/attachments",
            files={"file": file},
            request_options=request_options,
        )

    def download_claim_file(self, claim_id, file_name, request_options=None):
        """Download the binary contents of a claim attachment."""
        return self._get_binary(
            uri=("/post-purchase/v1/claims/" + self._path_param(claim_id)
                 + "/attachments/" + self._path_param(file_name) + "/download"),
            request_options=request_options,
        )