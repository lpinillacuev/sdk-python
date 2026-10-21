"""Unit tests for the Claims resource using a mock HTTP client."""
import unittest

from tests.base_client_test import BaseClientTest


class TestClaims(BaseClientTest):
    """Test Module: Claims"""

    def test_get_claim_reasons(self):
        self.mock_get({"id": "reason-1"})

        result = self.sdk.claims().get_claim_reasons("reason/1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/reasons/reason%2F1",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_search_claims(self):
        self.mock_get({"results": []})
        filters = {
            "id": 123, "type": "claims", "stage": "claim",
            "status": "opened", "limit": 10, "offset": 5,
        }

        result = self.sdk.claims().search_claims(filters=filters)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/search",
            kwargs["url"],
        )
        self.assertEqual(filters, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim(self):
        self.mock_get({"id": 123})

        result = self.sdk.claims().get_claim(123)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_evidence(self):
        self.mock_get([{"id": "evidence-1"}])

        result = self.sdk.claims().get_claim_evidence("claim/123")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/claim%2F123/evidences",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_mediation_resolutions(self):
        self.mock_get([{"id": "resolution-1"}])

        result = self.sdk.claims().get_claim_mediation_resolutions(123)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/expected-resolutions",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_messages(self):
        self.mock_get([{"id": "message-1"}])

        result = self.sdk.claims().get_claim_messages(123)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/messages",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_history(self):
        self.mock_get([{"id": "history-1"}])

        result = self.sdk.claims().get_claim_history(123)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/status_history",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_attach_claim_file(self):
        self.mock_http.request.return_value = {
            "status": 201, "response": {"file_id": "file-1"},
        }
        file = ("receipt.pdf", b"%PDF-1.4", "application/pdf")

        result = self.sdk.claims().attach_claim_file("claim/123", file)

        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual(("POST",), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/"
            "claim%2F123/attachments",
            kwargs["url"],
        )
        self.assertEqual({"file": file}, kwargs["files"])
        self.assertNotIn("Content-type", kwargs["headers"])
        self.assertEqual(201, result["status"])

    def test_get_claim_file(self):
        self.mock_get({"file_name": "report.pdf"})

        result = self.sdk.claims().get_claim_file(123, "folder/report.pdf")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/"
            "attachments/folder%2Freport.pdf",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_download_claim_file(self):
        file_content = b"%PDF-1.4\x00\xff"
        self.mock_http.get_binary.return_value = {
            "status": 200, "response": file_content,
        }

        result = self.sdk.claims().download_claim_file("claim/123", "folder/report.pdf")

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/"
            "claim%2F123/attachments/folder%2Freport.pdf/download",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(file_content, result["response"])


if __name__ == "__main__":
    unittest.main()