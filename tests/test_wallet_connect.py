"""Wire-level tests for the Wallet Connect resource through the SDK."""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.resources import WalletConnect
from tests.base_client_test import BaseClientTest


class TestWalletConnect(BaseClientTest):
    """Wallet Connect routes keep query, header, path and JSON body separate."""

    def test_create_wallet_agreement(self):
        self.mock_post({"agreement_id": "agr-1", "agreement_uri": "https://example.com/approve"}, 200)
        options = RequestOptions(platform_id="platform-1")
        payload = {"return_uri": "https://example.com/return", "external_flow_id": "flow-1"}

        resource = self.sdk.wallet_connect()
        self.assertIsInstance(resource, WalletConnect)
        result = resource.create_wallet_agreement(payload, client_id="client-1", request_options=options)

        self.assertEqual(200, result["status"])
        self.assertEqual("agr-1", result["response"]["agreement_id"])
        self.assertEqual("https://example.com/approve", result["response"]["agreement_uri"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/agreements", kwargs["url"])
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])
        self.assertEqual(payload, json.loads(kwargs["data"]))

    def test_delete_wallet_agreement(self):
        self.mock_delete(status=200)
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().delete_wallet_agreement(
            "agr/1", client_id="client-1", request_options=options
        )

        self.assertEqual(200, result["status"])
        self.mock_http.delete.assert_called_once()
        kwargs = self.mock_http.delete.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agr%2F1",
            kwargs["url"],
        )
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])

    def test_get_wallet_agreement(self):
        agreement = {"id": "agr-1", "status": "active", "external_flow_id": "flow-1"}
        self.mock_get(agreement)
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().get_wallet_agreement(
            "agr/1", client_id="client-1", request_options=options
        )

        self.assertEqual(200, result["status"])
        self.assertEqual(agreement, result["response"])
        self.mock_http.get.assert_called_once()
        kwargs = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agr%2F1",
            kwargs["url"],
        )
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])

    def test_create_wallet_payer_token(self):
        self.mock_post({"payer_token": "payer-1"}, 200)
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().create_wallet_payer_token(
            "agr/1", {"code": "auth-code"}, request_options=options
        )

        self.assertEqual(200, result["status"])
        self.assertEqual("payer-1", result["response"]["payer_token"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agr%2F1/payer_token",
            kwargs["url"],
        )
        self.assertEqual({"code": "auth-code"}, json.loads(kwargs["data"]))
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_validate_wallet_coupon(self):
        coupon = {"status": "active", "description": "Offer", "legal_terms": "Terms"}
        self.mock_post(coupon, 200)

        result = self.sdk.wallet_connect().validate_wallet_coupon(
            {"id": "coupon-1"}, payer_token="payer-1"
        )

        self.assertEqual(200, result["status"])
        self.assertEqual(coupon, result["response"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/coupons", kwargs["url"])
        self.assertEqual({"id": "coupon-1"}, json.loads(kwargs["data"]))
        self.assertEqual("payer-1", kwargs["headers"]["x-payer-token"])
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_create_wallet_discount(self):
        discount = {
            "discount": {"amount": 5.0, "coupon_id": "coupon-1", "type": "fixed"},
            "currency_id": "ARS",
            "transaction_amount": 95.0,
            "legal_terms": "Terms",
        }
        self.mock_post(discount, 200)

        result = self.sdk.wallet_connect().create_wallet_discount(
            {"coupon": "coupon-1", "amount": 100.0}, payer_token="payer-1"
        )

        self.assertEqual(200, result["status"])
        self.assertEqual(discount, result["response"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/discounts", kwargs["url"])
        self.assertEqual({"coupon": "coupon-1", "amount": 100.0}, json.loads(kwargs["data"]))
        self.assertEqual("payer-1", kwargs["headers"]["x-payer-token"])
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])


if __name__ == "__main__":
    unittest.main()