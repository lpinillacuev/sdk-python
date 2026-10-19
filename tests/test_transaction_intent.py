"""Wire-level tests for transaction intent disbursements."""
import json

from mercadopago.resources import TransactionIntent
from tests.base_client_test import BaseClientTest


class TestTransactionIntent(BaseClientTest):
    """Exercises the transaction intent resource through the SDK factory."""

    def test_process_transaction_intent(self):
        payload = {
            "transaction": {
                "amount": 100.0,
                "currency_id": "BRL",
                "receiver": {"id": "receiver-1"},
            },
            "point_of_interaction": {"type": "PIX"},
            "external_reference": "PAYOUT-001",
        }
        response = {"id": "intent-1"}
        self.mock_post(response, status=201)

        resource = self.sdk.transaction_intent()
        self.assertIsInstance(resource, TransactionIntent)
        result = resource.process_transaction_intent(payload)

        self.assertEqual(result["status"], 201)
        self.assertEqual(result["response"], response)
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual(kwargs["url"], "https://api.mercadopago.com/v1/transaction-intents/process")
        self.assertEqual(json.loads(kwargs["data"]), payload)
        self.assertEqual(kwargs["headers"]["Content-type"], "application/json")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer TEST_TOKEN")

    def test_get_transaction_intent(self):
        response = {"id": "intent/1", "status": "processed"}
        self.mock_get(response, status=200)

        resource = self.sdk.transaction_intent()
        self.assertIsInstance(resource, TransactionIntent)
        result = resource.get_transaction_intent("intent/1")

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["response"], response)
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual(kwargs["url"], "https://api.mercadopago.com/v1/transaction-intents/intent%2F1")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer TEST_TOKEN")