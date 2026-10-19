"""Customer address resource for the MercadoPago API.

Wraps the address endpoints under ``/v1/customers/{customer_id}/addresses``.
"""
from mercadopago.core import MPBase


class CustomerAddress(MPBase):
    """Manages addresses attached to a customer profile."""

    def list_all(self, customer_id, request_options=None):
        """Lists the customer's addresses."""
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id) + "/addresses",
            request_options=request_options,
        )

    def create(self, customer_id, address_object, request_options=None):
        """Creates an address for a customer from an Address dictionary."""
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._post(
            uri="/v1/customers/" + self._path_param(customer_id) + "/addresses",
            data=address_object,
            request_options=request_options,
        )

    def delete(self, customer_id, address_id, request_options=None):
        """Deletes a customer's address; the response need not contain JSON."""
        return self._delete(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            request_options=request_options,
        )

    def get(self, customer_id, address_id, request_options=None):
        """Retrieves one of a customer's addresses."""
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            request_options=request_options,
        )

    def update(self, customer_id, address_id, address_object, request_options=None):
        """Updates a customer's address from an Address dictionary."""
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._put(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            data=address_object,
            request_options=request_options,
        )