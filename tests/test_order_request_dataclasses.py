"""Offline tests for Order request dataclass serialization and compatibility."""
import dataclasses
import json
import unittest

import mercadopago
from mercadopago.http import HttpClient
from mercadopago.resources.item import ItemRequest
from mercadopago.resources.order_automatic_payments import OrderAutomaticPayments
from mercadopago.resources.order_create import OrderCreateRequest, order_request_to_dict
from mercadopago.resources.order_integration_data import OrderIntegrationData, OrderSponsor
from mercadopago.resources.order_stored_credential import OrderStoredCredential
from mercadopago.resources.order_subscription_data import (
    OrderInvoicePeriod,
    OrderSubscriptionData,
    OrderSubscriptionSequence,
)
from mercadopago.resources.order_transaction import (
    OrderPaymentMethodRequest,
    OrderPaymentRequest,
    OrderTransactionRequest,
)
from mercadopago.resources.order_transaction_security import OrderTransactionSecurity
from mercadopago.resources.payer import (
    PayerAddress,
    PayerIdentification,
    PayerPhone,
    PayerRequest,
)
from mercadopago.resources.shipment import (
    ShipmentAddress,
    ShipmentFreeMethod,
    ShipmentRequest,
)


class _CapturingHttpClient(HttpClient):
    """HttpClient stub that captures request bodies without network access."""

    def __init__(self):
        self.last_url = None
        self.last_data = None
        self.last_headers = None
        self.last_method = None

    def post(self, url, headers, data=None, params=None, timeout=None,
             maxretries=None, retry_on=None, backoff_factor=None):
        del params, timeout, maxretries, retry_on, backoff_factor
        self.last_method = "POST"
        self.last_url = url
        self.last_headers = headers
        self.last_data = data
        return {"status": 201, "response": {"id": "ORDER_ID", "status": "processed"}}


def _make_sdk():
    http = _CapturingHttpClient()
    return mercadopago.SDK("TEST_TOKEN", http_client=http), http


class TestOrderRequestDataclasses(unittest.TestCase):
    def test_nested_resources_use_snake_case_and_filter_none(self):
        request = OrderCreateRequest(
            type="online",
            total_amount="200.00",
            external_reference="ORDER-1",
            payer=PayerRequest(
                email="buyer@example.com",
                identification=PayerIdentification(type="CPF", number="123"),
                phone=PayerPhone(area_code="11", number="999999999"),
                address=PayerAddress(zip_code="0000", street_name="Main"),
            ),
            items=[ItemRequest(title="A book", unit_price="200.00", quantity=1)],
            shipments=ShipmentRequest(
                mode="me2",
                free_shipping=False,
                free_methods=[ShipmentFreeMethod(id=1)],
                address=ShipmentAddress(street_name="Main", zip_code="0000"),
            ),
            config={
                "online": {
                    "transaction_security": order_request_to_dict(
                        OrderTransactionSecurity(validation="complete")
                    )
                }
            },
        )

        payload = order_request_to_dict(request)

        self.assertEqual(payload["type"], "online")
        self.assertEqual(payload["total_amount"], "200.00")
        self.assertEqual(payload["external_reference"], "ORDER-1")
        self.assertEqual(payload["items"][0]["unit_price"], "200.00")
        self.assertEqual(payload["payer"]["phone"]["area_code"], "11")
        self.assertNotIn("last_name", payload["payer"])
        self.assertNotIn("description", payload["items"][0])
        self.assertEqual(payload["shipments"]["free_methods"], [{"id": 1}])
        self.assertFalse(payload["shipments"]["free_shipping"])
        self.assertNotIn("dimensions", payload["shipments"])
        self.assertEqual(
            payload["config"]["online"]["transaction_security"],
            {"validation": "complete"},
        )

    def test_dict_path_remains_backward_compatible(self):
        sdk, http = _make_sdk()
        order_data = {
            "type": "online",
            "total_amount": "200.00",
            "transactions": {"payments": [{"amount": "200.00"}]},
        }

        result = sdk.order().create(order_data)

        self.assertEqual(result["status"], 201)
        self.assertEqual(json.loads(http.last_data), order_data)

    def test_typed_and_dict_paths_serialize_identically(self):
        typed = OrderCreateRequest(
            type="online",
            total_amount="50.00",
            transactions=OrderTransactionRequest(
                payments=[
                    OrderPaymentRequest(
                        amount="50.00",
                        payment_method=OrderPaymentMethodRequest(
                            id="visa", type="credit_card", installments=1
                        ),
                        automatic_payments=OrderAutomaticPayments(
                            payment_profile_id="PROFILE"
                        ),
                        stored_credential=OrderStoredCredential(
                            payment_initiator="merchant", first_payment=False
                        ),
                        subscription_data=OrderSubscriptionData(
                            invoice_id="INV-1",
                            subscription_sequence=OrderSubscriptionSequence(
                                number=1, total=12
                            ),
                            invoice_period=OrderInvoicePeriod(type="monthly", period=1),
                        ),
                    )
                ]
            ),
            integration_data=OrderIntegrationData(
                integrator_id="INT-1", sponsor=OrderSponsor(id="SPONSOR-1")
            ),
        )
        equivalent = {
            "type": "online",
            "total_amount": "50.00",
            "transactions": {
                "payments": [{
                    "amount": "50.00",
                    "payment_method": {
                        "id": "visa", "type": "credit_card", "installments": 1
                    },
                    "automatic_payments": {"payment_profile_id": "PROFILE"},
                    "stored_credential": {
                        "payment_initiator": "merchant", "first_payment": False
                    },
                    "subscription_data": {
                        "invoice_id": "INV-1",
                        "subscription_sequence": {"number": 1, "total": 12},
                        "invoice_period": {"type": "monthly", "period": 1},
                    },
                }]
            },
            "integration_data": {
                "integrator_id": "INT-1", "sponsor": {"id": "SPONSOR-1"}
            },
        }
        typed_sdk, typed_http = _make_sdk()
        dict_sdk, dict_http = _make_sdk()

        typed_sdk.order().create(typed)
        dict_sdk.order().create(equivalent)

        typed_payload = json.loads(typed_http.last_data)
        self.assertEqual(typed_payload, json.loads(dict_http.last_data))
        payment = typed_payload["transactions"]["payments"][0]
        self.assertEqual(payment["automatic_payments"], {"payment_profile_id": "PROFILE"})
        self.assertFalse(payment["stored_credential"]["first_payment"])
        self.assertEqual(payment["subscription_data"]["invoice_period"]["period"], 1)
        self.assertEqual(typed_payload["integration_data"]["sponsor"]["id"], "SPONSOR-1")
        self.assertNotIn("expiration_time", payment)

    def test_custom_idempotency_key_is_preserved(self):
        sdk, http = _make_sdk()
        options = mercadopago.config.RequestOptions(
            access_token="TEST_TOKEN",
            custom_headers={"x-idempotency-key": "order-request-1"},
        )

        sdk.order().create({"type": "online"}, options)

        self.assertEqual(http.last_headers["x-idempotency-key"], "order-request-1")

    def test_helper_rejects_non_dataclass(self):
        with self.assertRaises(TypeError):
            order_request_to_dict({"type": "online"})

    def test_create_rejects_invalid_payload_type(self):
        sdk, _ = _make_sdk()
        with self.assertRaises(ValueError):
            sdk.order().create("not-a-dict")

    def test_dataclasses_asdict_keeps_snake_case(self):
        data = dataclasses.asdict(
            OrderIntegrationData(platform_id="PLATFORM", sponsor=OrderSponsor(id="1"))
        )
        self.assertIn("platform_id", data)
        self.assertNotIn("platformId", data)


if __name__ == "__main__":
    unittest.main()