"""Payment Methods resource for the MercadoPago API.

Wraps the ``/v1/payment_methods`` endpoint to list the payment methods
available for the authenticated account (credit cards, debit cards,
bank transfers, cash, etc.).
"""
from mercadopago.core import MPBase


class PaymentMethods(MPBase):
    """Lists payment methods available to the authenticated seller.

    The returned list varies by country and account configuration.  Use
    it to display accepted payment options in your checkout UI.
    """

    def list_all(self, request_options=None):
        """Retrieves all available payment methods.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of payment method objects (id, name, type,
            status, thumbnail, etc.).
        """
        return self._get(uri="/v1/payment_methods", request_options=request_options)

    def get_installments(
            self, payment_method_id, amount, issuer_id=None, bin=None,
            request_options=None):
        """Retrieves installment options for a payment method and amount.

        Args:
            payment_method_id: Payment method identifier.
            amount: Transaction amount used to calculate installment options.
            issuer_id: Optional card issuer identifier.
            bin: Optional first digits of the card number.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Available installment options.
        """
        filters = {
            "payment_method_id": payment_method_id,
            "amount": amount,
        }
        filters.update({
            key: value
            for key, value in (("issuer_id", issuer_id), ("bin", bin))
            if value is not None
        })

        return self._get(
            uri="/v1/payment_methods/installments",
            filters=filters,
            request_options=request_options,
        )
