"""Unit tests for the Terminals resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestTerminals(BaseClientTest):
    """Test Module: Terminals"""

    def test_create_point_refund_intent(self):
        self.mock_post({"id": "refund-001", "status": "OPEN"}, status=200)
        payload = {"payment_id": 12345, "amount": 10.50}

        result = self.sdk.terminals().create_point_refund_intent("device-001", payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/devices/device-001/refund",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_cancel_point_refund_intent(self):
        self.mock_delete({"id": "refund-001"}, status=200)

        result = self.sdk.terminals().cancel_point_refund_intent(
            "device-001", "refund-001"
        )

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/devices/device-001/refund/refund-001",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_point_refund_intent(self):
        self.mock_get({"id": "refund-001", "status": "OPEN"})

        result = self.sdk.terminals().get_point_refund_intent("refund-001")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/refund/refund-001",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_terminal_action(self):
        self.mock_post({"id": "action-001", "status": "pending"}, status=200)
        payload = {
            "type": "PRINT_INFO",
            "external_reference": "print-001",
            "config": {"device_id": "device-001"},
            "content": {"source": "https://example.com/receipt.png"},
        }

        result = self.sdk.terminals().create_terminal_action(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/terminals/v1/actions", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_create_terminal_action_print_dte(self):
        self.mock_post({"id": "action-002", "status": "pending"}, status=200)
        payload = {
            "type": "PRINT_DTE",
            "external_reference": "print-002",
            "config": {"device_id": "device-001"},
            "content": {"dte_data": "PGR0ZT48L2R0ZT4="},
        }

        result = self.sdk.terminals().create_terminal_action(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/terminals/v1/actions", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_get_terminal_action(self):
        self.mock_get({"id": "action-001", "status": "printed"})

        result = self.sdk.terminals().get_terminal_action("action/001")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions/action%2F001",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_cancel_terminal_action(self):
        self.mock_post({"id": "action-001"}, status=200)

        result = self.sdk.terminals().cancel_terminal_action("action/001")

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions/action%2F001/cancel",
            kwargs["url"],
        )
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