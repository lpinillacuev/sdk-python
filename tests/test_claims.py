"""Unit tests for the Claims resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestClaims(BaseClientTest):
    """Test Module: Claims"""

    def test_get_claim_reasons(self):
        self.mock_get({"id": "damaged"})

        result = self.sdk.claims().get_claim_reasons("damaged/other")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/reasons/damaged%2Fother",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_search_claims(self):
        self.mock_get({"results": []})
        filters = {
            "id": 123,
            "type": "claims",
            "stage": "claim",
            "status": "opened",
            "limit": 20,
            "offset": 10,
        }

        result = self.sdk.claims().search_claims(filters)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/search",
            kwargs["url"],
        )
        self.assertEqual(filters, kwargs["params"])
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
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_request_claim_mediation(self):
        self.mock_post({"id": "1"}, status=200)

        result = self.sdk.claims().request_claim_mediation("12/3")

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/actions/open-dispute",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_send_claim_message(self):
        self.mock_post({"id": "1"})
        message = {"message": "Tracking is available", "attachments": ["file-1"]}

        result = self.sdk.claims().send_claim_message(123, message, application_id="app-1")

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/actions/send-message",
            kwargs["url"],
        )
        self.assertEqual(message, json.loads(kwargs["data"]))
        self.assertEqual({"application_id": "app-1"}, kwargs["params"])
        self.assertEqual(201, result["status"])

    def test_download_claim_file(self):
        content = b"\x00\xff%PDF-1.7\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": content}

        result = self.sdk.claims().download_claim_file("12/3", "receipt/a.pdf")

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/attachments/receipt%2Fa.pdf/download",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])
        self.assertEqual(content, result["response"])

    def test_get_claim_file(self):
        self.mock_get({"file_id": "file-1"})

        result = self.sdk.claims().get_claim_file("12/3", "receipt/a.pdf")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/attachments/receipt%2Fa.pdf",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_attach_claim_file(self):
        self.mock_http.request.return_value = {
            "status": 201,
            "response": {"file_id": "file-1", "file_name": "receipt.pdf"},
        }
        file = ("receipt.pdf", b"PDF contents", "application/pdf")

        result = self.sdk.claims().attach_claim_file("12/3", file)

        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual(("POST",), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/attachments",
            kwargs["url"],
        )
        self.assertEqual({"file": file}, kwargs["files"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(201, result["status"])

    def test_get_claim_evidence(self):
        self.mock_get([{"id": "1"}])

        result = self.sdk.claims().get_claim_evidence("12/3")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/evidences",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_get_claim_mediation_resolutions(self):
        self.mock_get([{"id": "resolution-1"}])

        result = self.sdk.claims().get_claim_mediation_resolutions("12/3")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/expected-resolutions",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_get_claim_messages(self):
        self.mock_get([{"id": "message-1"}])

        result = self.sdk.claims().get_claim_messages("12/3")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/messages",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_get_claim_history(self):
        self.mock_get([{"status": "opened"}])

        result = self.sdk.claims().get_claim_history("12/3")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/12%2F3/status_history",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_upload_shipping_evidence(self):
        self.mock_post({"id": "1"})
        evidence = {"type": "tracking_code", "value": "TRACK-123"}

        result = self.sdk.claims().upload_shipping_evidence(123, evidence)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/actions/evidences",
            kwargs["url"],
        )
        self.assertEqual(evidence, json.loads(kwargs["data"]))
        self.assertIsNone(kwargs["params"])
        self.assertEqual(201, result["status"])


if __name__ == "__main__":
    unittest.main()