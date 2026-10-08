"""Unit tests for the Refund resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestRefund(BaseClientTest):
    """Test Module: Refund"""

    def test_list_all(self):
        fixture = self.load_fixture("refund_list_all.json")
        self.mock_get(fixture)

        result = self.sdk.refund().list_all(123)

        self.assertEqual(200, result["status"])
        self.mock_http.get.assert_called_once()
        call = self.mock_http.get.call_args
        self.assertTrue(call.kwargs["url"].endswith("/v1/payments/123/refunds"))

    def test_get_escapes_payment_and_refund_path_parameters(self):
        fixture = self.load_fixture("refund_get.json")
        self.mock_get(fixture)

        result = self.sdk.refund().get("payment/../123", "refund/../456")

        self.assertEqual(200, result["status"])
        self.mock_http.get.assert_called_once()
        call = self.mock_http.get.call_args
        self.assertTrue(
            call.kwargs["url"].endswith(
                "/v1/payments/payment%2F..%2F123/refunds/refund%2F..%2F456"
            )
        )

    def test_create_full_refund_sends_empty_object(self):
        fixture = self.load_fixture("refund_create.json")
        self.mock_post(fixture, status=201)

        result = self.sdk.refund().create(123)

        self.assertEqual(201, result["status"])
        self.mock_http.post.assert_called_once()
        call = self.mock_http.post.call_args
        self.assertTrue(call.kwargs["url"].endswith("/v1/payments/123/refunds"))
        self.assertEqual({}, json.loads(call.kwargs["data"]))

    def test_create_partial_refund(self):
        fixture = self.load_fixture("refund_create.json")
        self.mock_post(fixture, status=201)

        self.sdk.refund().create(123, {"amount": 50.0})

        call = self.mock_http.post.call_args
        self.assertEqual({"amount": 50.0}, json.loads(call.kwargs["data"]))

    def test_create_raises_for_non_dict_refund_object(self):
        with self.assertRaises(ValueError):
            self.sdk.refund().create(123, "not-a-dict")


if __name__ == "__main__":
    unittest.main()