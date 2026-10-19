"""Wire-level tests for payout batch and transaction operations."""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.resources import Payout
from tests.base_client_test import BaseClientTest


class TestPayout(BaseClientTest):
    """Payout API requests through the SDK factory."""

    def test_create_payout(self):
        payload = {
            "external_reference": "batch-123",
            "transactions": [{
                "amount": 12.5,
                "beneficiary": {"email": "recipient@example.com"},
                "currency_id": "ARS",
                "payment_method_id": "account_money",
            }],
        }
        response = {"id": "payout-123"}
        self.mock_post(response, status=201)
        payout = self.sdk.payout()

        self.assertIsInstance(payout, Payout)
        result = payout.create_payout(payload)

        self.assertEqual({"status": 201, "response": response}, result)
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v1/payouts", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_list_payout_transactions(self):
        response = ["transaction-result"]
        self.mock_get(response, status=200)
        options = RequestOptions(custom_headers={"x-test-header": "payouts"})

        result = self.sdk.payout().list_payout_transactions("batch/1", options)

        self.assertEqual({"status": 200, "response": response}, result)
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/batch%2F1/transactions",
            kwargs["url"],
        )
        self.assertEqual("payouts", kwargs["headers"]["x-test-header"])
        self.assertIsNone(kwargs["params"])

    def test_cancel_payout_transaction(self):
        response = "cancelled"
        self.mock_put(response, status=200)

        result = self.sdk.payout().cancel_payout_transaction("batch/1", "tx/2")

        self.assertEqual({"status": 200, "response": response}, result)
        self.mock_http.put.assert_called_once()
        kwargs = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/batch%2F1/transactions/tx%2F2/cancel",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertIsNone(kwargs["params"])


if __name__ == "__main__":
    unittest.main()