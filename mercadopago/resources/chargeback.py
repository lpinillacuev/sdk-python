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

    def update(self, chargeback_id, chargeback_object, request_options=None):
        """Uploads documentation for a chargeback dispute.

        Args:
            chargeback_id: Unique chargeback identifier.
            chargeback_object: Dict containing the ``files`` documentation list.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated chargeback response.
        """
        if not isinstance(chargeback_object, dict):
            raise ValueError("Param chargeback_object must be a Dictionary")

        return self._put(
            uri="/v1/chargebacks/" + self._path_param(chargeback_id),
            data=chargeback_object,
            request_options=request_options,
        )

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
