"""Unit tests for the QRIntegrator resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestQRIntegrator(BaseClientTest):
    """Test Module: QRIntegrator"""

    def test_get_qr_integrator_config(self):
        self.mock_get({"callback_url": "https://example.com/callback"})

        result = self.sdk.qr_integrator().get_qr_integrator_config()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/instore/integrator", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_qr_integrator_config(self):
        payload = {
            "callback_url": "https://example.com/callback",
            "notification_url": "https://example.com/notifications",
        }
        self.mock_http.request.return_value = {
            "status": 200,
            "response": {"callback_url": payload["callback_url"]},
        }

        result = self.sdk.qr_integrator().create_qr_integrator_config(payload)

        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual(("PATCH",), args)
        self.assertEqual("https://api.mercadopago.com/instore/integrator", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()