"""Customer address resource for the MercadoPago API."""
from mercadopago.core import MPBase


class CustomerAddress(MPBase):
    """Lists and creates addresses associated with a customer."""

    def list_customer_addresses(self, customer_id, request_options=None):
        """Lists the addresses belonging to a customer.

        Args:
            customer_id: Unique customer identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of customer addresses and HTTP status.
        """
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id) + "/addresses",
            request_options=request_options,
        )

    def delete_customer_address(self, customer_id, address_id, request_options=None):
        """Deletes an address belonging to a customer.

        Args:
            customer_id: Unique customer identifier.
            address_id: Unique address identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response and HTTP status.
        """
        return self._delete(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            request_options=request_options,
        )

    def get_customer_address(self, customer_id, address_id, request_options=None):
        """Retrieves an address belonging to a customer.

        Args:
            customer_id: Unique customer identifier.
            address_id: Unique address identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Customer address and HTTP status.
        """
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            request_options=request_options,
        )

    def update_customer_address(self, customer_id, address_id, address_object,
                                request_options=None):
        """Updates an address belonging to a customer.

        Args:
            customer_id: Unique customer identifier.
            address_id: Unique address identifier.
            address_object: Address dict with zip_code, street_name,
                street_number, city, state, and country.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a ``dict``.

        Returns:
            dict: Updated customer address and HTTP status.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._put(
            uri="/v1/customers/" + self._path_param(customer_id)
            + "/addresses/" + self._path_param(address_id),
            data=address_object,
            request_options=request_options,
        )

    def create_customer_address(self, customer_id, address_object, request_options=None):
        """Creates an address on a customer profile.

        Args:
            customer_id: Unique customer identifier.
            address_object: Address dict with zip_code, street_name,
                street_number, city, state, and country.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a ``dict``.

        Returns:
            dict: Created address and HTTP status.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._post(
            uri="/v1/customers/" + self._path_param(customer_id) + "/addresses",
            data=address_object,
            request_options=request_options,
        )