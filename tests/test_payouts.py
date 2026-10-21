"""Unit tests for the Payouts resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestPayouts(BaseClientTest):
    """Test Module: Payouts"""

    def test_create_payout(self):
        self.mock_post({"id": "1"}, status=201)
        payload = {
            "external_reference": "batch-1",
            "transactions": [{
                "amount": 100.0,
                "beneficiary": {"id": "recipient-1"},
                "currency_id": "ARS",
                "payment_method_id": "account_money",
            }],
        }

        result = self.sdk.payouts().create_payout(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v1/payouts", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_list_payout_transactions(self):
        self.mock_get({"results": []})

        result = self.sdk.payouts().list_payout_transactions("batch/1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/batch%2F1/transactions",
            kwargs["url"],
        )
        self.assertIsNone(kwargs.get("data"))
        self.assertEqual(200, result["status"])

    def test_cancel_payout_transaction(self):
        self.mock_put({"id": "transaction-1"})

        result = self.sdk.payouts().cancel_payout_transaction("batch/1", "tx/2")

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/batch%2F1/transactions/tx%2F2/cancel",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_process_transaction_intent(self):
        self.mock_post({"id": "intent-1"}, status=201)
        payload = {
            "external_reference": "PAYOUT-001",
            "point_of_interaction": {"type": "PIX"},
            "transaction": {"amount": 100.0, "currency_id": "BRL"},
        }

        result = self.sdk.payouts().process_transaction_intent(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/transaction-intents/process",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])


if __name__ == "__main__":
    unittest.main()