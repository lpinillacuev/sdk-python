"""Customer address resource for the MercadoPago API."""
from mercadopago.core import MPBase


class CustomerAddress(MPBase):
    """Manages addresses attached to customer profiles."""

    def list_customer_addresses(self, customer_id, request_options=None):
        """Lists the addresses of a customer.

        Args:
            customer_id: Identifier of the customer.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Customer address list.
        """
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id) + "/addresses",
            request_options=request_options,
        )

    def create_customer_address(self, customer_id, address_object, request_options=None):
        """Adds an address to a customer.

        Args:
            customer_id: Identifier of the customer.
            address_object: Dict containing the address fields.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a ``dict``.

        Returns:
            dict: Created address.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._post(
            uri="/v1/customers/" + self._path_param(customer_id) + "/addresses",
            data=address_object,
            request_options=request_options,
        )

    def get_customer_address(self, customer_id, address_id, request_options=None):
        """Retrieves one customer address.

        Args:
            customer_id: Identifier of the customer.
            address_id: Identifier of the address.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Requested address.
        """
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            request_options=request_options,
        )

    def update_customer_address(self, customer_id, address_id, address_object,
                                request_options=None):
        """Updates one customer address.

        Args:
            customer_id: Identifier of the customer.
            address_id: Identifier of the address.
            address_object: Dict containing the address fields to update.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a ``dict``.

        Returns:
            dict: Updated address.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._put(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            data=address_object,
            request_options=request_options,
        )

    def delete_customer_address(self, customer_id, address_id, request_options=None):
        """Deletes one customer address.

        Args:
            customer_id: Identifier of the customer.
            address_id: Identifier of the address.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response.
        """
        return self._delete(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            request_options=request_options,
        )