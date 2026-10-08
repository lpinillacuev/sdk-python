"""Unit tests for the CardToken resource using a mock HTTP client."""
import json
import unittest

from mercadopago.config import RequestOptions
from tests.base_client_test import BaseClientTest


class TestCardToken(BaseClientTest):
    """Test Module: CardToken"""

    def test_get(self):
        fixture = self.load_fixture("card_token_get.json")
        self.mock_get(fixture)
        result = self.sdk.card_token().get("a78sd6f1a9s8d7f1a")
        self.assertEqual(200, result["status"])
        resp = result["response"]
        self.assertEqual("a78sd6f1a9s8d7f1a", resp["id"])
        self.assertEqual("503143", resp["first_six_digits"])
        self.assertEqual("6351", resp["last_four_digits"])
        self.assertEqual(11, resp["expiration_month"])
        self.assertEqual(2030, resp["expiration_year"])
        self.assertTrue(resp["luhn_validation"])
        self.assertEqual("active", resp["status"])
        self.assertIn("date_created", resp)
        self.assertIn("date_due", resp)
        self.assertIn("cardholder", resp)
        self.assertEqual("APRO", resp["cardholder"]["name"])
        self.mock_http.get.assert_called_once()
        call = self.mock_http.get.call_args.kwargs
        self.assertEqual(
            "https://api.mercadopago.com/v1/card_tokens/a78sd6f1a9s8d7f1a",
            call["url"],
        )
        self.assertEqual("Bearer TEST_TOKEN", call["headers"]["Authorization"])

    def test_create(self):
        fixture = self.load_fixture("card_token_create.json")
        self.mock_post(fixture, status=201)
        card_token_object = {
            "card_number": "5031433215406351",
            "security_code": "123",
            "expiration_year": 2030,
            "expiration_month": 11,
            "cardholder": {"name": "APRO"},
        }
        request_options = RequestOptions(
            custom_headers={"X-Public-Key": "TEST_PUBLIC_KEY"},
        )

        result = self.sdk.card_token().create(card_token_object, request_options)

        self.assertEqual(201, result["status"])
        self.mock_http.post.assert_called_once()
        call = self.mock_http.post.call_args.kwargs
        self.assertEqual("https://api.mercadopago.com/v1/card_tokens", call["url"])
        self.assertEqual(card_token_object, json.loads(call["data"]))
        self.assertFalse(
            any(name.lower() == "authorization" for name in call["headers"])
        )
        self.assertEqual("TEST_PUBLIC_KEY", call["headers"]["X-Public-Key"])

    def test_create_raises_for_non_dict(self):
        with self.assertRaisesRegex(ValueError, "must be a Dictionary"):
            self.sdk.card_token().create("raw-card-data")


if __name__ == "__main__":
    unittest.main()