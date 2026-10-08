"""Unit tests for the MerchantOrder resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestMerchantOrder(BaseClientTest):
    """Test Module: MerchantOrder"""

    def test_create(self):
        fixture = self.load_fixture("merchant_order_create.json")
        self.mock_post(fixture, status=201)
        merchant_order_object = {
            "external_reference": "ext-ref-001",
            "preference_id": "843382748-18d90a57-a4ce-4718",
            "marketplace": "NONE",
            "notification_url": "https://example.com/notifications",
            "sponsor_id": 123456,
            "payer": {"id": 987654321, "email": "buyer@example.com"},
            "site_id": "MLB",
            "items": [{"title": "Point Mini", "quantity": 1, "unit_price": 58.80}],
            "additional_info": "Merchant order test",
            "application_id": "123456789",
        }

        result = self.sdk.merchant_order().create(merchant_order_object)

        self.assertEqual(201, result["status"])
        resp = result["response"]
        self.assertEqual(4049696864, resp["id"])
        self.assertEqual("opened", resp["status"])
        self.assertEqual(58.80, resp["total_amount"])
        self.assertIsInstance(resp["items"], list)
        self.assertIn("date_created", resp)
        call = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/merchant_orders", call.kwargs["url"])
        self.assertEqual(merchant_order_object, json.loads(call.kwargs["data"]))

    def test_get(self):
        fixture = self.load_fixture("merchant_order_get.json")
        self.mock_get(fixture)

        result = self.sdk.merchant_order().get(merchant_order_id=4049696864)

        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual(4049696864, resp["id"])
        self.assertEqual("opened", resp["status"])
        self.assertEqual("ext-ref-001", resp["external_reference"])
        self.assertEqual("843382748-18d90a57-a4ce-4718", resp["preference_id"])
        self.assertIsInstance(resp["payments"], list)
        self.assertIsInstance(resp["items"], list)
        self.assertEqual("Point Mini", resp["items"][0]["title"])
        self.assertEqual(58.80, resp["total_amount"])
        self.assertEqual(0.0, resp["paid_amount"])
        self.assertIn("date_created", resp)
        self.assertIn("notification_url", resp)
        self.assertEqual(
            "https://api.mercadopago.com/merchant_orders/4049696864",
            self.mock_http.get.call_args.kwargs["url"],
        )

    def test_get_accepts_legacy_merchan_order_id_keyword(self):
        fixture = self.load_fixture("merchant_order_get.json")
        self.mock_get(fixture)

        result = self.sdk.merchant_order().get(merchan_order_id=4049696864)

        self.assertEqual(200, result["status"])
        self.assertEqual(
            "https://api.mercadopago.com/merchant_orders/4049696864",
            self.mock_http.get.call_args.kwargs["url"],
        )

    def test_update(self):
        fixture = self.load_fixture("merchant_order_update.json")
        self.mock_put(fixture)
        merchant_order_object = {
            "external_reference": "ext-updated",
            "additional_info": "Updated merchant order",
        }

        result = self.sdk.merchant_order().update(
            merchant_order_id=4049696864,
            merchant_order_object=merchant_order_object,
        )

        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual(4049696864, resp["id"])
        self.assertEqual("ext-updated", resp["external_reference"])
        self.assertIn("last_updated", resp)
        call = self.mock_http.put.call_args
        self.assertEqual(
            "https://api.mercadopago.com/merchant_orders/4049696864",
            call.kwargs["url"],
        )
        self.assertEqual(merchant_order_object, json.loads(call.kwargs["data"]))

    def test_update_accepts_legacy_merchan_order_id_keyword(self):
        fixture = self.load_fixture("merchant_order_update.json")
        self.mock_put(fixture)
        merchant_order_object = {"external_reference": "ext-updated"}

        result = self.sdk.merchant_order().update(
            merchan_order_id=4049696864,
            merchant_order_object=merchant_order_object,
        )

        self.assertEqual(200, result["status"])
        call = self.mock_http.put.call_args
        self.assertEqual(
            "https://api.mercadopago.com/merchant_orders/4049696864",
            call.kwargs["url"],
        )
        self.assertEqual(merchant_order_object, json.loads(call.kwargs["data"]))

    def test_search_with_all_documented_filters(self):
        fixture = self.load_fixture("merchant_order_search.json")
        self.mock_get(fixture)
        filters = {
            "status": "opened",
            "preference_id": "843382748-18d90a57-a4ce-4718",
            "application_id": "123456789",
            "payer_id": 987654321,
            "sponsor_id": 123456,
            "external_reference": "ext-ref-001",
            "site_id": "MLB",
            "marketplace": "NONE",
            "date_created_from": "2024-01-01T00:00:00Z",
            "date_created_to": "2024-01-31T23:59:59Z",
            **dict(
                last_updated_from="2024-01-01T00:00:00Z",
                last_updated_to="2024-01-31T23:59:59Z",
            ),
            "limit": 30,
            "offset": 0,
        }

        result = self.sdk.merchant_order().search(filters)

        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertIn("elements", resp)
        self.assertEqual(4049696864, resp["elements"][0]["id"])
        call = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/merchant_orders/search",
            call.kwargs["url"],
        )
        self.assertEqual(filters, call.kwargs["params"])

    def test_deprecated_qr_operations_use_documented_verbs_and_uris(self):
        order = {"title": "Order", "total_amount": 10}

        self.mock_post({"id": "order-id"})
        self.sdk.merchant_order().create_instore_order(123, "order/id", order)
        post = self.mock_http.post.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/mpmobile/instore/qr/123/order%2Fid",
            post["url"],
        )
        self.assertEqual(order, json.loads(post["data"]))

        self.mock_delete({})
        self.sdk.merchant_order().delete_instore_order(123, "order/id")
        self.assertEqual(
            "https://api.mercadopago.com/mpmobile/instore/qr/123/order%2Fid",
            self.mock_http.delete.call_args.kwargs["url"],
        )

    def test_qr_integrator_operations_use_documented_verbs_and_uris(self):
        order = {"title": "Order", "total_amount": 10}

        self.mock_put({"id": "order-id"})
        self.sdk.merchant_order().create_instore_order_v2(
            123, "store/id", "pos/id", order
        )
        put = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/instore/qr/seller/collectors/123/"
            "stores/store%2Fid/pos/pos%2Fid/orders",
            put["url"],
        )
        self.assertEqual(order, json.loads(put["data"]))

        expected_url = (
            "https://api.mercadopago.com/instore/qr/seller/collectors/123/"
            "pos/pos%2Fid/orders"
        )
        self.mock_get({"id": "order-id"})
        self.sdk.merchant_order().get_instore_order_v2(123, "pos/id")
        self.assertEqual(expected_url, self.mock_http.get.call_args.kwargs["url"])

        self.mock_delete({})
        self.sdk.merchant_order().delete_instore_order_v2(123, "pos/id")
        self.assertEqual(expected_url, self.mock_http.delete.call_args.kwargs["url"])

    def test_qr_order_operations_use_documented_verbs_and_uris(self):
        qr_object = {"title": "Order", "total_amount": 10}
        expected_url = (
            "https://api.mercadopago.com/instore/orders/qr/seller/collectors/"
            "123/pos/pos%2Fid/qrs"
        )

        self.mock_post({"qr_data": "000201"})
        self.sdk.merchant_order().create_qr_tramma_dynamic(
            123, "pos/id", qr_object
        )
        post = self.mock_http.post.call_args.kwargs
        self.assertEqual(expected_url, post["url"])
        self.assertEqual(qr_object, json.loads(post["data"]))

        self.mock_put({"id": "order-id"})
        self.sdk.merchant_order().create_dynamic_qr_order(
            123, "pos/id", qr_object
        )
        put = self.mock_http.put.call_args.kwargs
        self.assertEqual(expected_url, put["url"])
        self.assertEqual(qr_object, json.loads(put["data"]))

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.merchant_order().create("not-a-dict")

    def test_update_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.merchant_order().update(4049696864, "not-a-dict")


if __name__ == "__main__":
    unittest.main()