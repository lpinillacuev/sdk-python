"""Store resource for the MercadoPago API."""
from mercadopago.core import MPBase


class Store(MPBase):
    """Retrieves MercadoPago stores."""

    def get_store(self, id, request_options=None):
        """Retrieves a store by its ID."""
        return self._get(
            uri="/stores/" + self._path_param(id),
            request_options=request_options,
        )