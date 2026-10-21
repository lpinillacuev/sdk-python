"""Payout batch and transaction intent API resource."""
from mercadopago.core import MPBase


class Payouts(MPBase):
    """Manages payout transactions and transaction intents."""

    def get_transaction_intent(self, intent_id, request_options=None):
        """Retrieves the status of a transaction intent.

        Args:
            intent_id: Identifier of the transaction intent.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Transaction intent response.
        """
        return self._get(
            uri="/v1/transaction-intents/" + self._path_param(intent_id),
            request_options=request_options)

    def create_payout(self, payout_object, request_options=None):
        """Creates a batch of payout transactions.

        Args:
            payout_object: Dict containing transactions and external_reference.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created payout batch response.
        """
        if not isinstance(payout_object, dict):
            raise ValueError("Param payout_object must be a Dictionary")

        return self._post(
            uri="/v1/payouts",
            data=payout_object,
            request_options=request_options)

    def list_payout_transactions(self, payout_id, request_options=None):
        """Lists the transactions in a payout batch.

        Args:
            payout_id: Identifier of the payout batch.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Payout transaction list response.
        """
        return self._get(
            uri="/v1/payouts/" + self._path_param(payout_id) + "/transactions",
            request_options=request_options)

    def cancel_payout_transaction(self, payout_id, transaction_id, request_options=None):
        """Cancels a payout transaction.

        Args:
            payout_id: Identifier of the payout batch.
            transaction_id: Identifier of the transaction to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancelled transaction response.
        """
        return self._put(
            uri="/v1/payouts/" + self._path_param(payout_id)
            + "/transactions/" + self._path_param(transaction_id) + "/cancel",
            request_options=request_options)

    def process_transaction_intent(self, intent_object, request_options=None):
        """Creates a disbursement transaction intent.

        Args:
            intent_object: Dict containing transaction and point_of_interaction.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created transaction intent response.
        """
        if not isinstance(intent_object, dict):
            raise ValueError("Param intent_object must be a Dictionary")

        return self._post(
            uri="/v1/transaction-intents/process",
            data=intent_object,
            request_options=request_options)