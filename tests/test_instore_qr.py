"""Wire-level tests for the in-store QR order endpoints."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestInstoreQR(BaseClientTest):
    """Verify each QR order operation uses its own verb and URL."""

    def test_create_qr_tramma_dynamic(self):
        self.mock_post({"id": "qr-1"})
        payload = {"external_reference": "order-1", "total_amount": 10}

        self.sdk.instore_qr().create_qr_tramma_dynamic(123, "pos/one", payload)

        self.mock_http.post.assert_called_once()
        args = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/instore/orders/qr/seller/collectors/123"
            "/pos/pos%2Fone/qrs", args["url"]
        )
        self.assertEqual(payload, json.loads(args["data"]))

    def test_create_dynamic_qr_order(self):
        self.mock_put({"id": "qr-2"})
        payload = {"external_reference": "order-2"}

        self.sdk.instore_qr().create_dynamic_qr_order(123, "pos/one", payload)

        self.mock_http.put.assert_called_once()
        self.mock_http.post.assert_not_called()
        args = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/instore/orders/qr/seller/collectors/123"
            "/pos/pos%2Fone/qrs", args["url"]
        )
        self.assertEqual(payload, json.loads(args["data"]))

    def test_confirm_cashout_qr(self):
        self.mock_post({"status": "confirmed"})
        payload = {"status": "confirmed"}

        self.sdk.instore_qr().confirm_cashout_qr("merchant/one", payload)

        self.mock_http.post.assert_called_once()
        args = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/instore/orders/merchant%2Fone/confirmation",
            args["url"],
        )
        self.assertEqual(payload, json.loads(args["data"]))

    def test_delete_instore_order_v2(self):
        self.mock_delete({})

        self.sdk.instore_qr().delete_instore_order_v2(123, "pos/one")

        self.mock_http.delete.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/instore/qr/seller/collectors/123"
            "/pos/pos%2Fone/orders",
            self.mock_http.delete.call_args.kwargs["url"],
        )

    def test_get_instore_order_v2(self):
        self.mock_get({"id": "order-1"})

        self.sdk.instore_qr().get_instore_order_v2(123, "pos/one")

        self.mock_http.get.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/instore/qr/seller/collectors/123"
            "/pos/pos%2Fone/orders",
            self.mock_http.get.call_args.kwargs["url"],
        )

    def test_create_instore_order_v2(self):
        self.mock_put({"id": "order-2"})
        payload = {"external_reference": "order-2"}

        self.sdk.instore_qr().create_instore_order_v2(
            123, "store/one", "pos/two", payload
        )

        self.mock_http.put.assert_called_once()
        args = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/instore/qr/seller/collectors/123"
            "/stores/store%2Fone/pos/pos%2Ftwo/orders", args["url"]
        )
        self.assertEqual(payload, json.loads(args["data"]))

    def test_delete_instore_order_v1(self):
        self.mock_delete({})

        self.sdk.instore_qr().delete_instore_order_v1(123, "external/one")

        self.mock_http.delete.assert_called_once()
        self.assertEqual(
            "https://api.mercadopago.com/mpmobile/instore/qr/123/external%2Fone",
            self.mock_http.delete.call_args.kwargs["url"],
        )

    def test_create_instore_order_v1(self):
        self.mock_put({"id": "order-3"})
        payload = {"external_reference": "order-3"}

        self.sdk.instore_qr().create_instore_order_v1(123, "external/one", payload)

        self.mock_http.put.assert_called_once()
        args = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/mpmobile/instore/qr/123/external%2Fone",
            args["url"],
        )
        self.assertEqual(payload, json.loads(args["data"]))


if __name__ == "__main__":
    unittest.main()