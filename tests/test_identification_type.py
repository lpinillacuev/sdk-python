"""Unit tests for the IdentificationType resource using a mock client."""
import unittest

from tests.base_client_test import BaseClientTest


class TestIdentificationType(BaseClientTest):
    """Test Module: IdentificationType"""

    def test_list_all_uses_exact_catalog_path_without_query(self):
        fixture = self.load_fixture("identification_type_list_all.json")
        self.mock_get(fixture)
        result = self.sdk.identification_type().list_all()
        self.assertEqual(200, result["status"])
        self.assertIsInstance(result["response"], list)
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/identification_types",
            call["url"],
        )
        self.assertIsNone(call["params"])
        self.assertIn("Authorization", call["headers"])


if __name__ == "__main__":
    unittest.main()