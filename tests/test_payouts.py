"""Unit tests for the Payouts resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestPayouts(BaseClientTest):
    """Test Module: Payouts"""

    def test_create_payout(self):
        self.mock_post({"id": "payout-1"}, status=201)
        payload = {
            "transactions": [{"amount": 100.0, "currency_id": "ARS"}],
            "external_reference": "batch-1",
        }

        result = self.sdk.payouts().create_payout(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v1/payouts", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_list_payout_transactions(self):
        self.mock_get({"transactions": []})

        result = self.sdk.payouts().list_payout_transactions("payout-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/payout-1/transactions",
            kwargs["url"],
        )
        self.assertEqual(200, result["status"])

    def test_cancel_payout_transaction(self):
        self.mock_put({"id": "transaction-1", "status": "cancelled"})

        result = self.sdk.payouts().cancel_payout_transaction(
            "payout-1", "transaction-1")

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/payout-1/"
            "transactions/transaction-1/cancel",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_get_transaction_intent(self):
        self.mock_get({"id": "intent-1", "status": "processed"})

        result = self.sdk.payouts().get_transaction_intent("intent-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v1/transaction-intents/intent-1",
            kwargs["url"],
        )
        self.assertEqual(200, result["status"])

    def test_process_transaction_intent(self):
        self.mock_post({"id": "intent-1"}, status=201)
        payload = {
            "transaction": {"amount": 100.0, "currency_id": "BRL"},
            "point_of_interaction": {"type": "PIX"},
            "external_reference": "intent-1",
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