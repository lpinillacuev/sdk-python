"""Unit tests for the WalletConnect resource using a mock HTTP client."""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.resources import WalletConnect
from tests.base_client_test import BaseClientTest


class TestWalletConnect(BaseClientTest):
    """Test Module: WalletConnect"""

    def test_create_wallet_agreement(self):
        self.mock_post({"agreement_id": "agreement-1"}, status=200)
        payload = {"return_uri": "https://example.com/return",
                   "external_flow_id": "flow-1"}
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().create_wallet_agreement(
            payload, client_id="client-1", request_options=options)

        self.assertIsInstance(self.sdk.wallet_connect(), WalletConnect)
        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/agreements",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])

    def test_delete_wallet_agreement(self):
        self.mock_delete({"id": "agreement-1"}, status=200)
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().delete_wallet_agreement(
            "agreement/1", filters={"client.id": "client-1"}, request_options=options)

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/agreements/agreement%2F1",
                         kwargs["url"])
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])

    def test_get_wallet_agreement(self):
        self.mock_get({"id": "agreement-1"})
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().get_wallet_agreement(
            "agreement-1", filters={"client.id": "client-1"}, request_options=options)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/agreements/agreement-1",
                         kwargs["url"])
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])

    def test_validate_wallet_coupon(self):
        self.mock_post({"status": "active"}, status=200)
        payload = {"id": "coupon-1"}
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().validate_wallet_coupon(
            payload, "payer-token-1", request_options=options)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/coupons",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("payer-token-1", kwargs["headers"]["x-payer-token"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])

    def test_create_wallet_discount(self):
        self.mock_post({"discount": {"amount": 10.0}}, status=200)
        payload = {"coupon": "coupon-1", "amount": 100.0}
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().create_wallet_discount(
            payload, "payer-token-1", request_options=options)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/discounts",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("payer-token-1", kwargs["headers"]["x-payer-token"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])

    def test_create_wallet_payer_token(self):
        self.mock_post({"payer_token": "token-1"}, status=200)
        payload = {"code": "authorization-code"}
        options = RequestOptions(platform_id="platform-1")

        result = self.sdk.wallet_connect().create_wallet_payer_token(
            "agreement-1", payload, request_options=options)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agreement-1/payer_token",
            kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()