"""Tests for Stores, POS, and QR operations exposed by User."""
import json
import warnings

from tests.base_client_test import BaseClientTest


class TestUser(BaseClientTest):
    """Verifies HTTP verbs, paths, query parameters, and request bodies."""

    def test_get(self):
        self.mock_get({"id": 12345})
        self.sdk.user().get()
        self.assertTrue(self.mock_http.get.call_args.kwargs["url"].endswith("/users/me"))

    def test_store_operations(self):
        user = self.sdk.user()
        body = {"name": "Main store"}

        self.mock_post({})
        user.create_store(123, body)
        call = self.mock_http.post.call_args.kwargs
        self.assertTrue(call["url"].endswith("/users/123/stores"))
        self.assertEqual(json.loads(call["data"]), body)

        self.mock_get({})
        user.get_store("store/1")
        self.assertTrue(
            self.mock_http.get.call_args.kwargs["url"].endswith("/stores/store%2F1")
        )

        user.search_stores(123, {"external_id": "main"})
        call = self.mock_http.get.call_args.kwargs
        self.assertTrue(call["url"].endswith("/users/123/stores/search"))
        self.assertEqual(call["params"], {"external_id": "main"})

        self.mock_put({})
        user.update_store(123, "store-1", body)
        call = self.mock_http.put.call_args.kwargs
        self.assertTrue(call["url"].endswith("/users/123/stores/store-1"))
        self.assertEqual(json.loads(call["data"]), body)

        self.mock_delete()
        user.delete_store(123, "store-1")
        self.assertTrue(
            self.mock_http.delete.call_args.kwargs["url"].endswith(
                "/users/123/stores/store-1"
            )
        )

    def test_pos_operations(self):
        user = self.sdk.user()
        body = {"name": "Register", "store_id": "store-1"}

        self.mock_get({})
        user.search_pos({"external_id": "pos-1"})
        call = self.mock_http.get.call_args.kwargs
        self.assertTrue(call["url"].endswith("/pos"))
        self.assertEqual(call["params"], {"external_id": "pos-1"})

        self.mock_post({})
        user.create_pos(body)
        self.assertEqual(json.loads(self.mock_http.post.call_args.kwargs["data"]), body)

        user.get_pos("pos/1")
        self.assertTrue(
            self.mock_http.get.call_args.kwargs["url"].endswith("/pos/pos%2F1")
        )

        self.mock_put({})
        user.update_pos("pos-1", body)
        self.assertTrue(
            self.mock_http.put.call_args.kwargs["url"].endswith("/pos/pos-1")
        )

        self.mock_delete()
        user.delete_pos("pos-1")
        self.assertTrue(
            self.mock_http.delete.call_args.kwargs["url"].endswith("/pos/pos-1")
        )

        user.list_pos(123)
        self.assertTrue(
            self.mock_http.get.call_args.kwargs["url"].endswith("/users/123/pos")
        )

    def test_qr_operations(self):
        user = self.sdk.user()
        body = {"status": "confirmed"}

        self.mock_get({})
        user.get_qr_integrator()
        self.assertTrue(
            self.mock_http.get.call_args.kwargs["url"].endswith("/instore/integrator")
        )

        self.mock_post({})
        user.confirm_cashout_qr("order/1", body)
        call = self.mock_http.post.call_args.kwargs
        self.assertTrue(
            call["url"].endswith("/instore/orders/order%2F1/confirmation")
        )
        self.assertEqual(json.loads(call["data"]), body)

    def test_deprecated_qr_operations(self):
        user = self.sdk.user()
        body = {"external_reference": "order-1"}

        self.mock_get({})
        user.get_instore_order_v2(123, "pos-1")
        self.assertTrue(
            self.mock_http.get.call_args.kwargs["url"].endswith(
                "/instore/qr/seller/collectors/123/pos/pos-1/orders"
            )
        )

        self.mock_delete()
        user.delete_instore_order_v2(123, "pos-1")
        self.assertTrue(
            self.mock_http.delete.call_args.kwargs["url"].endswith(
                "/instore/qr/seller/collectors/123/pos/pos-1/orders"
            )
        )

        self.mock_put({})
        user.create_instore_order_v1(123, "pos-1", body)
        self.assertTrue(
            self.mock_http.put.call_args.kwargs["url"].endswith(
                "/mpmobile/instore/qr/123/pos-1"
            )
        )

        user.create_instore_order_v2(123, "store-1", "pos-1", body)
        self.assertTrue(
            self.mock_http.put.call_args.kwargs["url"].endswith(
                "/instore/qr/seller/collectors/123/stores/store-1/pos/pos-1/orders"
            )
        )

        self.mock_post({})
        user.create_qr_tramma_dynamic(123, "pos-1", body)
        self.assertTrue(
            self.mock_http.post.call_args.kwargs["url"].endswith(
                "/instore/orders/qr/seller/collectors/123/pos/pos-1/qrs"
            )
        )

        self.mock_put({})
        user.create_dynamic_qr_order(123, "pos-1", body)
        self.assertTrue(
            self.mock_http.put.call_args.kwargs["url"].endswith(
                "/instore/orders/qr/seller/collectors/123/pos/pos-1/qrs"
            )
        )