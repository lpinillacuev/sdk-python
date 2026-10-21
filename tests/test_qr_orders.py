"""Unit tests for the QROrders resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestQROrders(BaseClientTest):
    """Test Module: QROrders"""

    def test_confirm_cashout_qr(self):
        payload = {"status": "confirmed"}
        self.mock_post({"id": "1"}, status=200)

        result = self.sdk.qr_orders().confirm_cashout_qr("order/../123", payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/instore/orders/order%2F..%2F123/confirmation",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()