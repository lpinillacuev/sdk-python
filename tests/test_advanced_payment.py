"""Unit tests for Advanced Payments and Wallet Connect operations."""
import json
from datetime import datetime
import unittest

from mercadopago.config import RequestOptions
from mercadopago.resources import AdvancedPayment
from tests.base_client_test import BaseClientTest


class TestAdvancedPayment(BaseClientTest):
    """Test Module: AdvancedPayment"""

    def test_sdk_factory_returns_advanced_payment(self):
        self.assertIsInstance(self.sdk.advanced_payment(), AdvancedPayment)

    def test_get(self):
        self.mock_get({"id": 999})
        self.sdk.advanced_payment().get(999)
        request = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/advanced_payments/999",
            request["url"],
        )
        self.assertIsNone(request["params"])

    def test_create(self):
        self.mock_post({"id": 999}, status=201)
        data = {"wallet_payment": {"transaction_amount": 100.0}}
        self.sdk.advanced_payment().create(data)
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/advanced_payments",
            request["url"],
        )
        self.assertEqual(data, json.loads(request["data"]))
        self.assertIn("x-idempotency-key", request["headers"])

    def test_update(self):
        self.mock_put({"id": 999})
        data = {"status": "cancelled"}
        self.sdk.advanced_payment().update(999, data)
        request = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/advanced_payments/999",
            request["url"],
        )
        self.assertEqual(data, json.loads(request["data"]))

    def test_create_wallet_agreement(self):
        self.mock_post({"agreement_id": "agreement-1"})
        data = {
            "return_uri": "https://example.com/return",
            "external_flow_id": "flow-1",
        }
        options = RequestOptions(
            access_token="token", platform_id="platform-1")
        self.sdk.advanced_payment().create_wallet_agreement(
            data, client_id="client-1", request_options=options)
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements",
            request["url"],
        )
        self.assertEqual({"client.id": "client-1"}, request["params"])
        self.assertEqual(data, json.loads(request["data"]))
        self.assertEqual("platform-1", request["headers"]["x-platform-id"])

    def test_get_wallet_agreement(self):
        self.mock_get({"id": "agreement-1"})
        self.sdk.advanced_payment().get_wallet_agreement(
            "agreement/1", client_id="client-1")
        request = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/"
            "agreement%2F1",
            request["url"],
        )
        self.assertEqual({"client.id": "client-1"}, request["params"])

    def test_delete_wallet_agreement(self):
        self.mock_delete({})
        self.sdk.advanced_payment().delete_wallet_agreement(
            "agreement-1", client_id="client-1")
        request = self.mock_http.delete.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/"
            "agreement-1",
            request["url"],
        )
        self.assertEqual({"client.id": "client-1"}, request["params"])

    def test_create_wallet_payer_token(self):
        self.mock_post({"payer_token": "payer-token"})
        data = {"code": "authorization-code"}
        self.sdk.advanced_payment().create_wallet_payer_token(
            "agreement-1", data)
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/"
            "agreement-1/payer_token",
            request["url"],
        )
        self.assertEqual(data, json.loads(request["data"]))

    def test_create_wallet_discount(self):
        self.mock_post({"discount": {"amount": 10.0}})
        data = {"coupon": "SAVE10", "amount": 100.0}
        options = RequestOptions(
            access_token="token",
            custom_headers={"x-payer-token": "payer-token"},
        )
        self.sdk.advanced_payment().create_wallet_discount(data, options)
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/discounts",
            request["url"],
        )
        self.assertEqual(data, json.loads(request["data"]))
        self.assertEqual("payer-token", request["headers"]["x-payer-token"])

    def test_validate_wallet_coupon(self):
        self.mock_post({"status": "active"})
        data = {"id": "SAVE10"}
        options = RequestOptions(
            access_token="token",
            custom_headers={"x-payer-token": "payer-token"},
        )
        self.sdk.advanced_payment().validate_wallet_coupon(data, options)
        request = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/coupons",
            request["url"],
        )
        self.assertEqual(data, json.loads(request["data"]))
        self.assertEqual("payer-token", request["headers"]["x-payer-token"])

    def test_capture_cancel_and_release_date(self):
        self.mock_put({"id": 999})
        self.sdk.advanced_payment().capture(999)
        self.assertEqual(
            {"capture": True},
            json.loads(self.mock_http.put.call_args.kwargs["data"]),
        )
        self.mock_http.put.reset_mock()
        self.sdk.advanced_payment().cancel(999)
        self.assertEqual(
            {"status": "cancelled"},
            json.loads(self.mock_http.put.call_args.kwargs["data"]),
        )
        self.mock_post({"id": 999})
        self.sdk.advanced_payment().update_release_date(
            999, datetime(2026, 9, 1))
        self.assertEqual(
            "https://api.mercadopago.com/v1/advanced_payments/999/disburses",
            self.mock_http.post.call_args.kwargs["url"],
        )

    def test_invalid_body_types(self):
        resource = self.sdk.advanced_payment()
        invalid_calls = (
            lambda: resource.create("invalid"),
            lambda: resource.update(1, "invalid"),
            lambda: resource.create_wallet_agreement("invalid"),
            lambda: resource.create_wallet_payer_token("id", "invalid"),
            lambda: resource.create_wallet_discount("invalid"),
            lambda: resource.validate_wallet_coupon("invalid"),
            lambda: resource.update_release_date(1, "invalid"),
        )
        for call in invalid_calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()