"""Identification Type resource for the MercadoPago API."""
from mercadopago.core import MPBase


class IdentificationType(MPBase):
    """Lists identification types for the authenticated credential's site."""

    def list_all(self, request_options=None):
        """Retrieves the identification-type catalog.

        The bearer-authenticated operation has no path, query, or body
        parameters and returns the catalog for the credential's site.
        """
        return self._get(
            uri="/v1/identification_types",
            request_options=request_options,
        )

    @property
    def request_options(self):
        """Default :class:`RequestOptions` for this resource instance."""
        return self.__request_options