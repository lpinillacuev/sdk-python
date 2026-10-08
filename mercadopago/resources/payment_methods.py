"""Payment Methods resource for MercadoPago payment catalogs."""
from mercadopago.core import MPBase


class PaymentMethods(MPBase):
    """Lists payment methods and retrieves installment options."""

    def list_all(self, request_options=None):
        """Retrieves payment methods available to the authenticated seller."""
        return self._get(uri="/v1/payment_methods", request_options=request_options)

    def get_installments(self, payment_method_id, amount, issuer_id=None,
                         bin=None, request_options=None):
        """Retrieves installment options for a payment method and amount.

        Args:
            payment_method_id: Payment method identifier, for example ``visa``.
            amount: Transaction amount used to calculate installment plans.
            issuer_id: Optional card issuer identifier.
            bin: Optional first six card digits.
            request_options: Per-call configuration overrides.
        """
        filters = {
            "payment_method_id": payment_method_id,
            "amount": amount,
        }
        optional_filters = {
            "issuer_id": issuer_id,
            "bin": bin,
        }
        filters.update(
            key_value for key_value in optional_filters.items()
            if key_value[1] is not None
        )

        return self._get(
            uri="/v1/payment_methods/installments",
            filters=filters,
            request_options=request_options,
        )