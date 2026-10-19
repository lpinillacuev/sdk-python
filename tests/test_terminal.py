"""Unit tests for terminal actions and listing through the Terminal resource."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestTerminal(BaseClientTest):
    """Test Module: Terminal"""

    def test_create_action(self):
        payload = {
            "type": "PRINT_INFO",
            "external_reference": "receipt-001",
            "config": {"device_id": "device-001"},
            "content": {"source": "https://example.com/receipt.png"},
        }
        response = {"id": "action-001", "status": "pending"}
        self.mock_post(response, status=200)

        result = self.sdk.terminal().create_action(payload)

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/terminals/v1/actions",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])

    def test_get_action(self):
        response = {
            "id": "action-001", "status": "printed",
            "type": "PRINT_INFO", "external_reference": "receipt-001",
            "date_created": "2025-01-01T12:00:00Z",
        }
        self.mock_get(response)

        result = self.sdk.terminal().get_action("action-001")

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.get.assert_called_once()
        self.assertEqual("https://api.mercadopago.com/terminals/v1/actions/action-001",
                         self.mock_http.get.call_args.kwargs["url"])

    def test_cancel_action(self):
        self.mock_post({}, status=200)

        result = self.sdk.terminal().cancel_action("action-001")

        self.assertEqual(200, result["status"])
        self.mock_http.post.assert_called_once()
        kwargs = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/terminals/v1/actions/"
                         "action-001/cancel", kwargs["url"])
        self.assertFalse(kwargs.get("data"))

    def test_list_all(self):
        response = {"terminals": [{
            "id": "device-001", "status": "active", "operating_mode": "PDV",
            "store_id": "store-001", "pos_id": 1,
        }]}
        self.mock_get(response)

        result = self.sdk.terminal().list_all()

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.get.assert_called_once()
        self.assertEqual("https://api.mercadopago.com/terminals/v1/list",
                         self.mock_http.get.call_args.kwargs["url"])

    def test_update_terminal_operation_mode(self):
        payload = {"terminals": [
            {"id": "device-001", "operating_mode": "PDV"},
            {"id": "device-002", "operating_mode": "STANDALONE"},
        ]}
        response = {"terminals": payload["terminals"]}
        self.mock_patch(response, status=200)

        result = self.sdk.terminal().update_terminal_operation_mode(payload)

        self.assertEqual(200, result["status"])
        self.assertEqual(response, result["response"])
        self.mock_http.patch.assert_called_once()
        kwargs = self.mock_http.patch.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/terminals/v1/setup",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])


if __name__ == "__main__":
    unittest.main()