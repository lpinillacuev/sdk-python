"""Offline tests for the QR Integrator configuration resource."""
import json
from unittest.mock import patch

from mercadopago.config import RequestOptions
from mercadopago.http.http_client import HttpClient
from mercadopago.resources import QRIntegrator
from tests.base_client_test import BaseClientTest


class TestQRIntegrator(BaseClientTest):
    """Exercise both configuration operations through the public SDK."""

    def test_accessor_uses_shared_client_and_options(self):
        resource = self.sdk.qr_integrator()
        self.assertIsInstance(resource, QRIntegrator)
        self.assertIs(resource.request_options, self.sdk.request_options)
        override = RequestOptions()
        override.access_token = "OVERRIDE_TOKEN"
        resource = self.sdk.qr_integrator(override)
        self.assertIs(resource.request_options, override)

    def test_get_returns_envelope_and_callback_url_from_response(self):
        config = {"callback_url": "https://example.com/qr/events"}
        self.mock_get(config)
        result = self.sdk.qr_integrator().get()
        self.assertEqual(200, result["status"])
        self.assertEqual(config, result["response"])
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith("/instore/integrator"))
        self.assertEqual("Bearer TEST_TOKEN", kwargs["headers"]["Authorization"])
        self.assertIsNone(kwargs["params"])
        self.mock_http.patch.assert_not_called()

    def test_get_forwards_request_options(self):
        options = RequestOptions()
        options.access_token = "OTHER_TOKEN"
        self.mock_get({"callback_url": "https://example.com/qr"})
        self.sdk.qr_integrator().get(request_options=options)
        self.assertEqual(
            "Bearer OTHER_TOKEN",
            self.mock_http.get.call_args.kwargs["headers"]["Authorization"],
        )

    def test_create_patches_json_config_with_request_options(self):
        body = {
            "callback_url": "https://example.com/qr/events",
            "notification_url": "https://example.com/legacy",
        }
        response = {"callback_url": body["callback_url"]}
        self.mock_http.patch.return_value = {"status": 200, "response": response}
        options = RequestOptions()
        options.access_token = "OTHER_TOKEN"
        result = self.sdk.qr_integrator().create(body, request_options=options)
        self.assertEqual({"status": 200, "response": response}, dict(result))
        self.mock_http.patch.assert_called_once()
        kwargs = self.mock_http.patch.call_args.kwargs
        self.assertTrue(kwargs["url"].endswith("/instore/integrator"))
        self.assertEqual("Bearer OTHER_TOKEN", kwargs["headers"]["Authorization"])
        self.assertEqual(body, json.loads(kwargs["data"]))
        self.assertIsNone(kwargs["params"])
        self.mock_http.post.assert_not_called()

    def test_create_rejects_non_dictionary_without_sending(self):
        for invalid in (None, "not-a-dict", ["callback_url"]):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    self.sdk.qr_integrator().create(invalid)
        self.mock_http.patch.assert_not_called()

    def test_http_client_patch_uses_patch_verb(self):
        client = HttpClient()
        envelope = {"status": 200, "response": {"callback_url": "https://example.com/qr"}}
        with patch.object(client, "request", return_value=envelope) as request:
            result = client.patch(
                "https://api.mercadopago.com/instore/integrator",
                {"Authorization": "Bearer TEST_TOKEN"},
                data='{"callback_url": "https://example.com/qr"}',
            )
        self.assertEqual(envelope, result)
        args, kwargs = request.call_args
        self.assertEqual("PATCH", args[0])
        self.assertEqual("https://api.mercadopago.com/instore/integrator", kwargs["url"])
        self.assertIn("callback_url", kwargs["data"])