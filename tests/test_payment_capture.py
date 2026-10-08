import json
import unittest
from unittest.mock import MagicMock

import mercadopago
from mercadopago.http.http_client import HttpClient


class TestPaymentCapture(unittest.TestCase):
    def setUp(self):
        self.mock_http = MagicMock(spec=HttpClient)
        self.mock_http.put.return_value = {
            "status": 200,
            "response": {"id": 123, "status": "approved"},
        }
        self.sdk = mercadopago.SDK("TEST_TOKEN", http_client=self.mock_http)

    def test_capture_full(self):
        result = self.sdk.payment().capture(123)

        self.assertEqual(result["status"], 200)
        call = self.mock_http.put.call_args.kwargs
        self.assertEqual(call["url"], "https://api.mercadopago.com/v1/payments/123")
        self.assertEqual(json.loads(call["data"]), {"capture": True})

    def test_capture_partial(self):
        result = self.sdk.payment().capture(123, amount=50.0)

        self.assertEqual(result["status"], 200)
        call = self.mock_http.put.call_args.kwargs
        self.assertEqual(call["url"], "https://api.mercadopago.com/v1/payments/123")
        self.assertEqual(
            json.loads(call["data"]),
            {"capture": True, "transaction_amount": 50.0},
        )


if __name__ == "__main__":
    unittest.main()