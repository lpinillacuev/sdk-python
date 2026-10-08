"""Unit tests for the OAuth resource using a mock HTTP client."""
import json
import unittest
from urllib.parse import parse_qs, urlparse

from tests.base_client_test import BaseClientTest


class TestOAuth(BaseClientTest):
    """Test Module: OAuth"""

    def test_get_authorization_url(self):
        url = self.sdk.oauth().get_authorization_url(
            app_id="my-app-id",
            redirect_uri="https://example.com/callback",
            random_id="csrf-state-123",
        )
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        self.assertEqual(
            "https://auth.mercadopago.com/authorization",
            parsed._replace(query="").geturl(),
        )
        self.assertEqual(["my-app-id"], params["client_id"])
        self.assertEqual(["code"], params["response_type"])
        self.assertEqual(["csrf-state-123"], params["state"])
        self.assertEqual(
            ["https://example.com/callback"], params["redirect_uri"]
        )

    def test_create_sends_exact_path_body_and_no_bearer_auth(self):
        fixture = self.load_fixture("oauth_create.json")
        self.mock_post(fixture, status=200)
        oauth_object = {
            "client_id": "1234567890",
            "client_secret": "TEST_CLIENT_SECRET",
            "code": "auth-code-123",
            "redirect_uri": "https://example.com/callback",
            "grant_type": "authorization_code",
        }
        result = self.sdk.oauth().create(oauth_object)
        self.assertEqual(200, result["status"])
        self.assertEqual("APP_USR-001", result["response"]["access_token"])
        call = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/oauth/token", call["url"])
        self.assertEqual(oauth_object, json.loads(call["data"]))
        self.assertIsNone(call["params"])
        self.assertNotIn("Authorization", call["headers"])

    def test_refresh_uses_token_operation_without_bearer_auth(self):
        fixture = self.load_fixture("oauth_create.json")
        self.mock_post(fixture, status=200)
        oauth_object = {
            "client_id": "1234567890",
            "client_secret": "TEST_CLIENT_SECRET",
            "refresh_token": "TG-001-test-refresh-token",
            "grant_type": "refresh_token",
        }
        self.sdk.oauth().refresh(oauth_object)
        call = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/oauth/token", call["url"])
        self.assertEqual(oauth_object, json.loads(call["data"]))
        self.assertNotIn("Authorization", call["headers"])

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.oauth().create("not-a-dict")

    def test_refresh_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.oauth().refresh("not-a-dict")


if __name__ == "__main__":
    unittest.main()