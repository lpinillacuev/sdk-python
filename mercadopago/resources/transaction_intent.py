"""Transaction intent resource for disbursements."""

from mercadopago.core import MPBase


class TransactionIntent(MPBase):
    """Process transaction intents and retrieve their status."""

    def process_transaction_intent(self, transaction_intent_object, request_options=None):
        """Process a transaction intent with a JSON request body."""
        if not isinstance(transaction_intent_object, dict):
            raise ValueError("Param transaction_intent_object must be a Dictionary")

        return self._post(
            uri="/v1/transaction-intents/process",
            data=transaction_intent_object,
            request_options=request_options,
        )

    def get_transaction_intent(self, intent_id, request_options=None):
        """Retrieve a transaction intent by its ID."""
        if not isinstance(intent_id, str):
            raise ValueError("Param intent_id must be a string")

        return self._get(
            uri="/v1/transaction-intents/" + self._path_param(intent_id),
            request_options=request_options,
        )