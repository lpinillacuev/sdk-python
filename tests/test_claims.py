"""Direct wire-level tests for claim file attachments."""
import io
import unittest
from unittest.mock import MagicMock

from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient
from mercadopago.sdk import SDK
from mercadopago.resources import Claims


class TestClaims(unittest.TestCase):
    """Tests multipart attachment uploads through the SDK factory."""

    def test_download_claim_file(self):
        client = HttpClient()
        client.get_binary = MagicMock(return_value=b"\x00PDF\xff")
        sdk = SDK("test-token", http_client=client)
        options = RequestOptions(access_token="override-token")

        result = sdk.claims().download_claim_file("42/7", "evidence 1.pdf", options)

        self.assertEqual(b"\x00PDF\xff", result)
        client.get_binary.assert_called_once()
        args, kwargs = client.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/42%2F7/attachments/evidence%201.pdf/download",
            kwargs["url"],
        )
        self.assertEqual("Bearer override-token", kwargs["headers"]["Authorization"])
        self.assertEqual(options.connection_timeout, kwargs["timeout"])
        self.assertEqual(options.max_retries, kwargs["maxretries"])
        self.assertEqual(options.retry_on, kwargs["retry_on"])

    def test_attach_claim_file(self):
        client = HttpClient()
        client.request = MagicMock(return_value={
            "status": 201,
            "response": {"file_id": "file-001", "file_name": "evidence.pdf"},
        })
        sdk = SDK("test-token", http_client=client)
        attachment = io.BytesIO(b"PDF contents")
        options = RequestOptions(access_token="override-token")

        self.assertIsInstance(sdk.claims(), Claims)
        result = sdk.claims().attach_claim_file("42", attachment, options)

        self.assertEqual(201, result["status"])
        self.assertEqual(
            {"file_id": "file-001", "file_name": "evidence.pdf"},
            result["response"],
        )
        client.request.assert_called_once()
        args, kwargs = client.request.call_args
        self.assertEqual(("POST",), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/42/attachments",
            kwargs["url"],
        )
        self.assertEqual({"file": attachment}, kwargs["files"])
        self.assertEqual("Bearer override-token", kwargs["headers"]["Authorization"])
        self.assertNotIn("Content-type", kwargs["headers"])
        self.assertNotIn("Content-Type", kwargs["headers"])
        self.assertEqual(options.connection_timeout, kwargs["timeout"])
        self.assertEqual(options.max_retries, kwargs["maxretries"])
        self.assertEqual(options.retry_on, kwargs["retry_on"])


if __name__ == "__main__":
    unittest.main()