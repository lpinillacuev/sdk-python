"""Wire-level tests for post-purchase claim operations."""
import json
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

from mercadopago.http import HttpClient
from mercadopago.sdk import SDK


BASE = "https://api.mercadopago.com/post-purchase/v1/claims"


class TestClaim(unittest.TestCase):
    """Verify claim resource routing, query parameters, and bodies."""

    def setUp(self):
        self.http = MagicMock(spec=HttpClient)
        self.http.get.return_value = {"status": 200, "response": {}}
        self.http.post.return_value = {"status": 201, "response": {}}
        self.sdk = SDK("test-token", http_client=self.http)
        self.claim = self.sdk.claim()

    def assert_get(self, path, params=None):
        """Check the authenticated GET URL and its query parameters."""
        self.http.get.assert_called_once()
        kwargs = self.http.get.call_args.kwargs
        self.assertEqual(BASE + path, kwargs["url"])
        self.assertEqual(params, kwargs["params"])
        self.assertIn("Authorization", kwargs["headers"])

    def assert_post(self, path, data=None, params=None):
        """Check the POST URL and JSON-encoded request body."""
        self.http.post.assert_called_once()
        kwargs = self.http.post.call_args.kwargs
        self.assertEqual(BASE + path, kwargs["url"])
        self.assertEqual(params, kwargs["params"])
        self.assertEqual(data, None if kwargs["data"] is None else json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_sdk_exposes_claim(self):
        from mercadopago.resources.claim import Claim
        self.assertIsInstance(self.claim, Claim)
        self.assertIsInstance(self.sdk.claim(), Claim)

    def test_get_claim_reasons(self):
        reason = {"id": "not_received", "description": "Not received"}
        self.http.get.return_value = {"status": 200, "response": reason}
        result = self.claim.get_claim_reasons("not/received")
        self.assertEqual(reason, result["response"])
        self.assert_get("/reasons/not%2Freceived")

    def test_search_claims(self):
        filters = {"id": 42, "type": "claims", "stage": "claim",
                   "status": "opened", "limit": 10, "offset": 5}
        page = {"results": [], "paging": {"total": 0}}
        self.http.get.return_value = {"status": 200, "response": page}
        result = self.claim.search_claims(filters)
        self.assertEqual(page, result["response"])
        self.assert_get("/search", filters)

    def test_get_claim(self):
        body = {"id": 42, "stage": "claim", "status": "opened"}
        self.http.get.return_value = {"status": 200, "response": body}
        self.assertEqual(body, self.claim.get_claim(42)["response"])
        self.assert_get("/42")

    def test_upload_shipping_evidence(self):
        payload = {"type": "tracking_code", "value": "TRACK-123"}
        self.assertEqual(201, self.claim.upload_shipping_evidence(42, payload)["status"])
        self.assert_post("/42/actions/evidences", payload)

    def test_request_claim_mediation(self):
        self.assertEqual(201, self.claim.request_claim_mediation(42)["status"])
        self.assert_post("/42/actions/open-dispute")

    def test_send_claim_message(self):
        payload = {"message": "Package shipped", "attachments": ["file-1"]}
        self.assertEqual(201, self.claim.send_claim_message(
            42, payload, application_id="app-1")["status"])
        self.assert_post("/42/actions/send-message", payload,
                         {"application_id": "app-1"})

    def test_attach_claim_file_uses_multipart(self):
        file = BytesIO(b"\x89PNG\r\n\x1a\n")
        file.name = "proof.png"
        metadata = {"file_id": "file-1", "file_name": "proof.png"}
        self.http.post.return_value = {"status": 201, "response": metadata}
        result = self.claim.attach_claim_file(42, file)
        self.assertEqual(metadata, result["response"])
        self.http.post.assert_called_once()
        kwargs = self.http.post.call_args.kwargs
        self.assertEqual(BASE + "/42/attachments", kwargs["url"])
        self.assertEqual(file, kwargs["files"]["file"])
        self.assertNotIn("Content-type", kwargs["headers"])
        self.assertIsNone(kwargs.get("data"))

    def test_get_claim_file_returns_metadata(self):
        metadata = {"file_id": "file-1", "file_name": "proof.png",
                    "content_type": "image/png"}
        self.http.get.return_value = {"status": 200, "response": metadata}
        self.assertEqual(metadata, self.claim.get_claim_file(42, "proof/a.png")["response"])
        self.assert_get("/42/attachments/proof%2Fa.png")

    def test_download_claim_file_returns_bytes(self):
        content = b"\x89PNG\x00\xff"
        self.http.get.return_value = {"status": 200, "response": content}
        result = self.claim.download_claim_file(42, "proof.png")
        self.assertEqual(content, result["response"])
        self.assert_get("/42/attachments/proof.png/download")
        self.assertEqual("application/octet-stream",
                         self.http.get.call_args.kwargs["headers"]["Accept"])

    def test_get_claim_evidence(self):
        evidence = [{"type": "tracking_code", "value": "TRACK-123"}]
        self.http.get.return_value = {"status": 200, "response": evidence}
        self.assertEqual(evidence, self.claim.get_claim_evidence(42)["response"])
        self.assert_get("/42/evidences")

    def test_get_claim_mediation_resolutions(self):
        resolutions = [{"id": "refund"}]
        self.http.get.return_value = {"status": 200, "response": resolutions}
        self.assertEqual(resolutions,
                         self.claim.get_claim_mediation_resolutions(42)["response"])
        self.assert_get("/42/expected-resolutions")

    def test_get_claim_messages(self):
        messages = [{"id": "message-1"}]
        self.http.get.return_value = {"status": 200, "response": messages}
        self.assertEqual(messages, self.claim.get_claim_messages(42)["response"])
        self.assert_get("/42/messages")

    def test_get_claim_history(self):
        history = [{"status": "opened"}]
        self.http.get.return_value = {"status": 200, "response": history}
        self.assertEqual(history, self.claim.get_claim_history(42)["response"])
        self.assert_get("/42/status_history")


class TestClaimTransport(unittest.TestCase):
    """Exercise actual requests transport for binary and JSON claim calls."""

    def setUp(self):
        self.session = patch("mercadopago.http.http_client.requests.Session").start()
        self.addCleanup(patch.stopall)
        self.response = self.session.return_value.__enter__.return_value.request.return_value
        self.response.status_code = 200
        self.sdk = SDK("test-token")

    def test_download_binary_does_not_parse_json(self):
        content = b"\x00\xff\x89PNG"
        self.response.content = content
        result = self.sdk.claim().download_claim_file(42, "proof.png")
        self.assertEqual(content, result["response"])
        self.response.json.assert_not_called()
        args, kwargs = self.session.return_value.__enter__.return_value.request.call_args
        self.assertEqual("GET", args[0])
        self.assertEqual(BASE + "/42/attachments/proof.png/download", args[1])
        self.assertEqual("application/octet-stream", kwargs["headers"]["Accept"])

    def test_multipart_sends_file_and_parses_json(self):
        self.response.status_code = 201
        self.response.content = b'{"file_id":"f1","file_name":"proof.png"}'
        self.response.json.return_value = {"file_id": "f1", "file_name": "proof.png"}
        file = BytesIO(b"image bytes")
        file.name = "proof.png"
        result = self.sdk.claim().attach_claim_file(42, file)
        self.assertEqual("f1", result["response"]["file_id"])
        self.response.json.assert_called_once_with()
        args, kwargs = self.session.return_value.__enter__.return_value.request.call_args
        self.assertEqual("POST", args[0])
        self.assertEqual(BASE + "/42/attachments", args[1])
        self.assertEqual(file, kwargs["files"]["file"])
        self.assertNotIn("Content-type", kwargs["headers"])

    def test_json_remains_default_after_binary_calls(self):
        self.response.content = b'{"id":42}'
        self.response.json.return_value = {"id": 42}
        self.assertEqual({"id": 42}, self.sdk.claim().get_claim(42)["response"])
        self.response.json.assert_called_once_with()
        args, kwargs = self.session.return_value.__enter__.return_value.request.call_args
        self.assertEqual("GET", args[0])
        self.assertEqual(BASE + "/42", args[1])
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])


if __name__ == "__main__":
    unittest.main()