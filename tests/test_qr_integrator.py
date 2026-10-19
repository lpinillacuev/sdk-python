"""Tests for QR integrator configuration GET and PATCH operations."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestQRIntegrator(BaseClientTest):
    """Exercise the SDK QR integrator resource with a mock transport."""

    def test_get_qr_integrator_config(self):
        config = {"callback_url": "https://example.com/callback"}
        self.mock_get(config)

        result = self.sdk.qr_integrator().get_qr_integrator_config()

        self.assertEqual(200, result["status"])
        self.assertEqual(config, result["response"])
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/instore/integrator", kwargs["url"])
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_create_qr_integrator_config(self):
        payload = {
            "callback_url": "https://example.com/callback",
            "notification_url": "https://example.com/notification",
        }
        self.mock_http.request.return_value = {
            "status": 200, "response": {"callback_url": payload["callback_url"]},
        }

        result = self.sdk.qr_integrator().create_qr_integrator_config(payload)

        self.assertEqual(200, result["status"])
        self.assertEqual(payload["callback_url"], result["response"]["callback_url"])
        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual("PATCH", args[0])
        self.assertEqual("https://api.mercadopago.com/instore/integrator", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_create_qr_integrator_config_without_notification_url(self):
        payload = {"callback_url": "https://example.com/callback"}
        self.mock_http.request.return_value = {"status": 200, "response": {}}

        self.sdk.qr_integrator().create_qr_integrator_config(payload)

        args, kwargs = self.mock_http.request.call_args
        self.assertEqual("PATCH", args[0])
        self.assertEqual(payload, json.loads(kwargs["data"]))


if __name__ == "__main__":
    unittest.main()