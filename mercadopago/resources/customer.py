"""Customer and address resources for the MercadoPago API.

Wraps ``/v1/customers`` endpoints to search, retrieve, create, update, and
delete customer records, plus the nested customer-address endpoints.
"""
from mercadopago.core import MPBase
from mercadopago.pagination.iterator import search_auto_paging_iter as _paging_iter


class Customer(MPBase):
    """Stores and manages customer profiles and their addresses."""

    def search(self, filters=None, request_options=None):
        """Searches customers by email and pagination filters."""
        return self._get(
            uri="/v1/customers/search",
            filters=filters,
            request_options=request_options,
        )

    def get(self, customer_id, request_options=None):
        """Retrieves a customer by ID."""
        return self._get(
            uri="/v1/customers/" + self._path_param(customer_id),
            request_options=request_options,
        )

    def create(self, customer_object, request_options=None):
        """Creates a customer from a request dictionary."""
        if not isinstance(customer_object, dict):
            raise ValueError("Param customer_object must be a Dictionary")

        return self._post(
            uri="/v1/customers",
            data=customer_object,
            request_options=request_options,
        )

    def update(self, customer_id, customer_object, request_options=None):
        """Updates a customer from a request dictionary."""
        if not isinstance(customer_object, dict):
            raise ValueError("Param customer_object must be a Dictionary")

        return self._put(
            uri="/v1/customers/" + self._path_param(customer_id),
            data=customer_object,
            request_options=request_options,
        )

    def delete(self, customer_id, request_options=None):
        """Deletes a customer using the API's nonstandard delete URI."""
        return self._delete(
            uri="/v1/customers/" + self._path_param(customer_id) + "/delete",
            request_options=request_options,
        )

    def create_address(self, customer_id, address_object, request_options=None):
        """Creates an address for a customer from a request dictionary."""
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._post(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses",
            data=address_object,
            request_options=request_options,
        )

    def list_addresses(self, customer_id, request_options=None):
        """Lists a customer's addresses."""
        return self._get(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses",
            request_options=request_options,
        )

    def get_address(self, customer_id, address_id, request_options=None):
        """Retrieves one customer address."""
        uri = self._address_uri(customer_id, address_id)
        return self._get(uri=uri, request_options=request_options)

    def update_address(
        self, customer_id, address_id, address_object, request_options=None
    ):
        """Updates a customer address from a request dictionary."""
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._put(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses/"
            f"{self._path_param(address_id)}",
            data=address_object,
            request_options=request_options,
        )

    def delete_address(self, customer_id, address_id, request_options=None):
        """Deletes a customer address and returns the API response."""
        uri = self._address_uri(customer_id, address_id)
        return self._delete(uri=uri, request_options=request_options)

    def search_auto_paging_iter(self, filters=None, request_options=None, limit=100):
        """Lazily yields all customers matching filters across all pages."""
        return _paging_iter(self.search, filters, request_options, limit)