"""Unit tests for the Terminals resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestTerminals(BaseClientTest):
    """Test Module: Terminals"""

    def test_update_terminal_operation_mode(self):
        payload = {"terminals": [{"id": "device-001", "operating_mode": "PDV"}]}
        self.mock_http.request.return_value = {"status": 200, "response": {}}

        result = self.sdk.terminals().update_terminal_operation_mode(payload)

        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual(("PATCH",), args)
        self.assertEqual("https://api.mercadopago.com/terminals/v1/setup", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_create_point_refund_intent(self):
        self.mock_post({"id": "refund-001", "status": "created"})

        result = self.sdk.terminals().create_point_refund_intent(
            "device-001", {"payment_id": 123, "amount": 25.5})

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/devices/"
            "device-001/refund", kwargs["url"])
        self.assertEqual(
            {"payment_id": 123, "amount": 25.5}, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_cancel_point_refund_intent(self):
        self.mock_delete({"id": "refund-001"})

        result = self.sdk.terminals().cancel_point_refund_intent(
            "device-001", "refund-001")

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/devices/"
            "device-001/refund/refund-001", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_point_refund_intent(self):
        self.mock_get({"id": "refund-001", "status": "created"})

        result = self.sdk.terminals().get_point_refund_intent("refund-001")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/refund/"
            "refund-001", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_terminal_action(self):
        from mercadopago.resources import Terminals

        payload = {
            "type": "PRINT_INFO",
            "external_reference": "print-001",
            "config": {"device_id": "device-001"},
            "content": {"source": "https://example.com/receipt.png"},
        }
        self.mock_post({"id": "action-001", "status": "pending"})

        resource = self.sdk.terminals()
        self.assertIsInstance(resource, Terminals)
        result = resource.create_terminal_action(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/terminals/v1/actions", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_get_terminal_action(self):
        self.mock_get({"id": "action-001", "status": "pending"})

        result = self.sdk.terminals().get_terminal_action("action/001")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions/action%2F001",
            kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_cancel_terminal_action(self):
        self.mock_post({"id": "action-001", "status": "cancelled"})

        result = self.sdk.terminals().cancel_terminal_action("action/001")

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions/"
            "action%2F001/cancel", kwargs["url"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_list_terminals(self):
        self.mock_get({"terminals": [{"id": "device-001"}]})

        result = self.sdk.terminals().list_terminals()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/terminals/v1/list", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()