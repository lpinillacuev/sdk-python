"""Payout resource for creating batches and managing their transactions."""

from mercadopago.core import MPBase


class Payout(MPBase):
    """Manages payout batches and their transactions."""

    def create_payout(self, payout_object, request_options=None):
        """Create a payout batch from an external reference and transactions.

        ``payout_object`` is a dict containing ``external_reference`` and a
        ``transactions`` list. Each transaction may specify ``amount``,
        ``beneficiary``, ``currency_id`` and ``payment_method_id``.
        """
        if not isinstance(payout_object, dict):
            raise ValueError("Param payout_object must be a Dictionary")

        return self._post(
            uri="/v1/payouts", data=payout_object, request_options=request_options
        )

    def list_payout_transactions(self, payout_id, request_options=None):
        """List the transactions in a payout batch."""
        return self._get(
            uri=f"/v1/payouts/{self._path_param(payout_id)}/transactions",
            request_options=request_options,
        )

    def cancel_payout_transaction(
        self, payout_id, transaction_id, request_options=None
    ):
        """Cancel a transaction in a payout batch."""
        return self._put(
            uri=f"/v1/payouts/{self._path_param(payout_id)}"
            f"/transactions/{self._path_param(transaction_id)}/cancel",
            request_options=request_options,
        )