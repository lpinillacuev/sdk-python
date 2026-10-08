"""PreApproval resource for the MercadoPago Subscriptions API.

Wraps ``/preapproval`` endpoints to search, retrieve, create, update, and
export preapproval (subscription) records.
"""
from mercadopago.core import MPBase
from mercadopago.pagination.iterator import search_auto_paging_iter as _paging_iter


class PreApproval(MPBase):
    """Manages subscriptions represented by the ``/preapproval`` API."""

    def __init__(self, request_options, http_client):
        MPBase.__init__(self, request_options, http_client)

    def search(self, filters=None, request_options=None):
        """Searches subscriptions matching the given query filters."""
        return self._get(
            uri="/preapproval/search",
            filters=filters,
            request_options=request_options,
        )

    def get(self, preapproval_id, request_options=None):
        """Retrieves a subscription by ID."""
        return self._get(
            uri="/preapproval/" + self._path_param(preapproval_id),
            request_options=request_options,
        )

    def create(self, preapproval_object, request_options=None):
        """Creates a subscription from a dictionary request body."""
        if not isinstance(preapproval_object, dict):
            raise ValueError("Param preapproval_object must be a Dictionary")

        return self._post(
            uri="/preapproval",
            data=preapproval_object,
            request_options=request_options,
        )

    def update(self, preapproval_id, preapproval_object, request_options=None):
        """Updates a subscription through ``PUT /preapproval/{id}``."""
        if not isinstance(preapproval_object, dict):
            raise ValueError("Param preapproval_object must be a Dictionary")

        return self._put(
            uri="/preapproval/" + self._path_param(preapproval_id),
            data=preapproval_object,
            request_options=request_options,
        )

    def export(
        self,
        collector_id,
        preapproval_plan_id=None,
        status=None,
        sort=None,
        request_options=None,
    ):
        """Exports subscriptions as CSV, preserving the transport bytes."""
        filters = {
            "collector_id": collector_id,
            "preapproval_plan_id": preapproval_plan_id,
            "status": status,
            "sort": sort,
        }
        return self._get(
            uri="/preapproval/export",
            filters={key: value for key, value in filters.items() if value is not None},
            request_options=request_options,
        )

    def search_auto_paging_iter(self, filters=None, request_options=None, limit=100):
        """Lazily yields all items matching *filters* across all pages."""
        return _paging_iter(self.search, filters, request_options, limit)