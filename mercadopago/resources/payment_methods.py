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

        This bearer-authenticated operation has no path, query, or body
        parameters.

        Args:
            request_options: Per-call configuration overrides, including
                bearer authentication headers.

        Returns:
            dict: List of payment method objects (id, name, type,
            status, thumbnail, etc.).
        """
        return self._get(uri="/v1/payment_methods", request_options=request_options)

    def get_installments(self, filters, request_options=None):
        """Retrieves installment options for a payment method and amount.

        Sends ``filters`` unchanged as query parameters. The OpenAPI operation
        requires ``payment_method_id`` and ``amount`` and optionally accepts
        ``issuer_id`` and ``bin``.
        """
        if not isinstance(filters, dict):
            raise ValueError("Filters must be a Dictionary")
        if "payment_method_id" not in filters or "amount" not in filters:
            raise ValueError("Filters must include payment_method_id and amount")

        return self._get(
            uri="/v1/payment_methods/installments",
            filters=filters,
            request_options=request_options,
        )
