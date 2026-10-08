"""Tests for Claims APIs and multipart/binary transport behavior."""
import unittest

from tests.base_client_test import BaseClientTest


class TestClaim(BaseClientTest):
    """Verify all claim, message, resolution, and shipping operations."""

    def test_json_get_operations(self):
        calls = (
            (lambda claim: claim.get(123), "/post-purchase/v1/claims/123"),
            (lambda claim: claim.search({"status": "opened"}),
             "/post-purchase/v1/claims/search"),
            (lambda claim: claim.get_reason("PNR"),
             "/post-purchase/v1/claims/reasons/PNR"),
            (lambda claim: claim.get_history(123),
             "/post-purchase/v1/claims/123/status_history"),
            (lambda claim: claim.get_evidence(123),
             "/post-purchase/v1/claims/123/evidences"),
            (lambda claim: claim.get_messages(123),
             "/post-purchase/v1/claims/123/messages"),
            (lambda claim: claim.get_file(123, "proof.pdf"),
             "/post-purchase/v1/claims/123/attachments/proof.pdf"),
            (lambda claim: claim.get_mediation_resolutions(123),
             "/post-purchase/v1/claims/123/expected-resolutions"),
        )
        for invoke, path in calls:
            with self.subTest(path=path):
                self.mock_http.reset_mock()
                self.mock_get({})
                invoke(self.sdk.claim())
                self.assertEqual(
                    "https://api.mercadopago.com" + path,
                    self.mock_http.get.call_args.kwargs["url"],
                )

    def test_send_message_has_json_and_application_id_query(self):
        self.mock_post({}, status=201)
        self.sdk.claim().send_message(123, {"message": "hello"}, "app-1")
        call = self.mock_http.post.call_args.kwargs
        self.assertEqual({"application_id": "app-1"}, call["params"])
        self.assertEqual('{"message": "hello"}', call["data"])

    def test_action_posts(self):
        self.mock_post({}, status=200)
        self.sdk.claim().request_mediation(123)
        self.assertTrue(self.mock_http.post.call_args.kwargs["url"].endswith(
            "/post-purchase/v1/claims/123/actions/open-dispute"))
        self.mock_http.reset_mock()
        self.mock_post({}, status=201)
        self.sdk.claim().upload_shipping_evidence(
            123, {"type": "tracking_code", "value": "TRACK"})
        call = self.mock_http.post.call_args.kwargs
        self.assertTrue(call["url"].endswith("/claims/123/actions/evidences"))
        self.assertEqual(
            '{"type": "tracking_code", "value": "TRACK"}', call["data"])

    def test_attach_file_uses_multipart(self):
        self.mock_post({}, status=201)
        file_value = ("proof.pdf", b"pdf", "application/pdf")
        self.sdk.claim().attach_file(123, file_value)
        call = self.mock_http.post.call_args.kwargs
        self.assertEqual({"file": file_value}, call["files"])
        self.assertNotIn("data", call)
        self.assertNotIn("Content-type", call["headers"])

    def test_download_file_returns_binary_response(self):
        self.mock_binary_get(b"file-data")
        result = self.sdk.claim().download_file(123, "proof.pdf")
        self.assertEqual(b"file-data", result["response"])
        call = self.mock_http.get.call_args.kwargs
        self.assertTrue(call["url"].endswith(
            "/claims/123/attachments/proof.pdf/download"))
        self.assertTrue(call["binary"])

    def test_path_parameters_are_escaped(self):
        self.mock_get({})
        self.sdk.claim().get_file(123, "../proof.pdf")
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith(
            "/claims/123/attachments/..%2Fproof.pdf"))


if __name__ == "__main__":
    unittest.main()