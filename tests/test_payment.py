"""Unit tests for the Payment resource using a mock HTTP client."""
import json
import unittest
import warnings

from mercadopago.config.request_options import RequestOptions
from tests.base_client_test import BaseClientTest


class TestPayment(BaseClientTest):
    """Test Module: Payment"""

    def test_get(self):
        fixture = self.load_fixture("payment_get.json")
        self.mock_get(fixture)
        result = self.sdk.payment().get(17014025134)
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual(17014025134, resp["id"])
        self.assertEqual("approved", resp["status"])
        self.assertEqual("accredited", resp["status_detail"])
        self.assertEqual("visa", resp["payment_method_id"])
        self.assertEqual("credit_card", resp["payment_type_id"])
        self.assertEqual("BRL", resp["currency_id"])
        self.assertEqual(58.80, resp["transaction_amount"])
        self.assertTrue(resp["captured"])
        self.assertFalse(resp["binary_mode"])
        self.assertEqual(1, resp["installments"])
        self.assertEqual("aggregator", resp["processing_mode"])
        self.assertEqual("test_user@testuser.com", resp["payer"]["email"])
        self.assertIn("transaction_details", resp)
        self.assertIn("card", resp)
        self.assertEqual("503143", resp["card"]["first_six_digits"])
        self.assertEqual("6351", resp["card"]["last_four_digits"])
        self.mock_http.get.assert_called_once()

    def test_get_sends_payment_id_in_path(self):
        self.mock_get({"id": 17014025134})
        request_options = RequestOptions(access_token="TEST_TOKEN")

        self.sdk.payment().get(17014025134, request_options=request_options)

        call = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/payments/17014025134",
            call["url"],
        )

    def test_get_preserves_expanded_gateway_network_data(self):
        self.mock_get(
            {
                "expanded": {
                    "gateway": {
                        "reference": {
                            "network_data": {
                                "transaction_id": "ABC123",
                                "transaction_link_id": "550e8400",
                            }
                        }
                    }
                }
            }
        )

        result = self.sdk.payment().get(17014025134)

        network_data = result["response"]["expanded"]["gateway"]["reference"]["network_data"]
        self.assertEqual("ABC123", network_data["transaction_id"])
        self.assertEqual("550e8400", network_data["transaction_link_id"])

    def test_search(self):
        fixture = self.load_fixture("payment_search.json")
        self.mock_get(fixture)
        filters = {
            "sort": "date_created",
            "criteria": "desc",
            "external_reference": "ORDER-001",
            "range": "date_created",
            "begin_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-01-31T23:59:59Z",
            "status": "approved",
            "store_id": "STORE-1",
            "pos_id": "POS-1",
            "collector.id": "123",
            "payer.id": "456",
            "limit": 30,
            "offset": 0,
        }
        result = self.sdk.payment().search(filters)
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertIn("results", resp)
        self.assertIn("paging", resp)
        self.assertEqual(1, resp["paging"]["total"])
        self.assertEqual(30, resp["paging"]["limit"])
        results = resp["results"]
        self.assertIsInstance(results, list)
        self.assertEqual(17014025134, results[0]["id"])
        self.assertEqual("approved", results[0]["status"])
        self.assertEqual("BRL", results[0]["currency_id"])
        self.mock_http.get.assert_called_once()
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v1/payments/search", call["url"])
        self.assertEqual(filters, call["params"])

    def test_create(self):
        fixture = self.load_fixture("payment_create.json")
        self.mock_post(fixture, status=201)
        payment_object = {
            "transaction_amount": 58.80,
            "payment_method_id": "visa",
            "token": "token-001",
            "installments": 1,
            "payer": {"email": "test_user@testuser.com"},
        }
        result = self.sdk.payment().create(payment_object)
        self.assertEqual(201, result["status"])
        resp = result["response"]
        self.assertEqual(17014025134, resp["id"])
        self.assertEqual("pending", resp["status"])
        self.assertEqual("pending_waiting_payment", resp["status_detail"])
        self.assertEqual(58.80, resp["transaction_amount"])
        self.assertEqual("visa", resp["payment_method_id"])
        self.assertEqual("BRL", resp["currency_id"])
        self.assertFalse(resp["captured"])
        self.assert_http_call(
            "post",
            "/v1/payments",
            data=json.dumps(payment_object),
        )

    def test_create_sends_idempotency_key_from_request_options(self):
        self.mock_post({"id": 17014025134}, status=201)
        payment_object = {
            "transaction_amount": 58.80,
            "payer": {"email": "test_user@testuser.com"},
        }
        request_options = RequestOptions(
            access_token="TEST_TOKEN",
            custom_headers={"X-Idempotency-Key": "create-payment-001"},
        )

        self.sdk.payment().create(payment_object, request_options=request_options)

        call = self.mock_http.post.call_args.kwargs
        self.assertEqual("create-payment-001", call["headers"]["X-Idempotency-Key"])
        self.assertEqual(payment_object, json.loads(call["data"]))

    def test_create_with_notification_url_warns(self):
        fixture = self.load_fixture("payment_create.json")
        self.mock_post(fixture, status=201)
        payment_object = {
            "transaction_amount": 58.80,
            "payment_method_id": "visa",
            "token": "token-001",
            "installments": 1,
            "payer": {"email": "test_user@testuser.com"},
            "notification_url": "https://example.com/notifications",
        }
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            self.sdk.payment().create(payment_object)
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))

    def test_update(self):
        fixture = self.load_fixture("payment_update.json")
        self.mock_put(fixture)
        result = self.sdk.payment().update(17014025134, {"status": "cancelled"})
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual(17014025134, resp["id"])
        self.assertEqual("cancelled", resp["status"])
        self.assertIn("date_last_updated", resp)
        self.mock_http.put.assert_called_once()

    def test_cancel(self):
        fixture = self.load_fixture("payment_update.json")
        self.mock_put(fixture)
        request_options = RequestOptions(
            access_token="TEST_TOKEN",
            custom_headers={"X-Idempotency-Key": "cancel-payment-001"},
        )

        result = self.sdk.payment().cancel(17014025134, request_options=request_options)

        self.assertEqual(200, result["status"])
        self.assertEqual("cancelled", result["response"]["status"])
        self.mock_http.put.assert_called_once()
        call = self.mock_http.put.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/payments/17014025134/cancellations",
            call["url"],
        )
        self.assertEqual({"status": "cancelled"}, json.loads(call["data"]))
        self.assertEqual("cancel-payment-001", call["headers"]["X-Idempotency-Key"])

    def test_capture(self):
        fixture = self.load_fixture("payment_get.json")
        self.mock_put(fixture)
        result = self.sdk.payment().capture(17014025134)
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual(17014025134, resp["id"])
        self.assertEqual("approved", resp["status"])
        self.mock_http.put.assert_called_once()

    def test_capture_with_amount(self):
        fixture = self.load_fixture("payment_get.json")
        self.mock_put(fixture)
        result = self.sdk.payment().capture(17014025134, amount=50.0)
        self.assertEqual(200, result["status"])
        self.mock_http.put.assert_called_once()

    def test_create_raises_for_non_dict(self):
        with self.assertRaises(ValueError):
            self.sdk.payment().create("not-a-dict")


if __name__ == "__main__":
    unittest.main()
