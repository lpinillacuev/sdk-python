"""Offline HTTP contract tests for QR integrator configuration."""
import json
import unittest
from unittest.mock import MagicMock

from mercadopago import SDK
from mercadopago.config.request_options import RequestOptions
from mercadopago.resources import QRIntegrator


class TestQRIntegrator(unittest.TestCase):
    """Verify the QR integrator resource uses the shared PATCH transport."""

    def test_create_qr_integrator_config(self):
        http_client = MagicMock()
        payload = {
            "callback_url": "https://example.com/qr/callback",
            "notification_url": "https://example.com/qr/notifications",
        }
        http_client.request.return_value = {"status": 200, "response": {"updated": True}}
        sdk = SDK("TEST_TOKEN", http_client=http_client)
        options = RequestOptions(
            access_token="OVERRIDE_TOKEN",
            custom_headers={"X-QR-Test": "enabled"},
        )

        resource = sdk.qr_integrator()
        self.assertIsInstance(resource, QRIntegrator)
        result = resource.create_qr_integrator_config(payload, request_options=options)

        http_client.request.assert_called_once()
        args, kwargs = http_client.request.call_args
        self.assertEqual(args, ("PATCH",))
        self.assertEqual(kwargs["url"], "https://api.mercadopago.com/instore/integrator")
        self.assertEqual(json.loads(kwargs["data"]), payload)
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer OVERRIDE_TOKEN")
        self.assertEqual(kwargs["headers"]["X-QR-Test"], "enabled")
        self.assertEqual(kwargs["headers"]["Content-type"], "application/json")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["response"], {"updated": True})


if __name__ == "__main__":
    unittest.main()