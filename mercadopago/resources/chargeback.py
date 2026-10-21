"""Chargeback resource for the MercadoPago API.

Wraps ``/v1/chargebacks`` endpoints to search and retrieve chargeback
records initiated by cardholders through their issuing bank.

`API reference
<https://www.mercadopago.com.br/developers/en/reference/chargebacks/>`_
"""
from mercadopago.core import MPBase


class Chargeback(MPBase):
    """Provides read access to chargeback disputes.

    Chargebacks are created by MercadoPago when a cardholder disputes a
    payment.  Use :meth:`search` and :meth:`get` to monitor and respond
    to disputes.
    """

    def search(self, filters=None, request_options=None):
        """Searches chargebacks matching the given filters.

        Args:
            filters: Query-string parameters (e.g. ``payment_id``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching chargebacks.
        """
        return self._get(uri="/v1/chargebacks/search", filters=filters,
                         request_options=request_options)

    def get(self, chargeback_id, request_options=None):
        """Retrieves a chargeback by its ID.

        Args:
            chargeback_id: Unique chargeback identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full chargeback object including status and amounts.
        """
        return self._get(uri="/v1/chargebacks/" + self._path_param(chargeback_id),
                         request_options=request_options)

    def update_chargeback(self, chargeback_id, chargeback_object, request_options=None):
        """Updates the documentation files for a chargeback.

        Args:
            chargeback_id: Unique chargeback identifier.
            chargeback_object (dict): JSON body containing the documentation files.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If chargeback_object is not a Dictionary.

        Returns:
            dict: Chargeback update response.
        """
        if not isinstance(chargeback_object, dict):
            raise ValueError("Param chargeback_object must be a Dictionary")

        return self._put(uri="/v1/chargebacks/" + self._path_param(chargeback_id),
                         data=chargeback_object, request_options=request_options)
