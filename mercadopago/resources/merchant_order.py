"""Merchant Order resource for the MercadoPago API.

Wraps ``/merchant_orders`` endpoints to search, retrieve, create, and
update merchant orders.  A merchant order groups one or more Checkout
Pro payments under a single business reference.

`API reference
<https://www.mercadopago.com/developers/en/reference>`_
"""
from mercadopago.core import MPBase
from mercadopago.pagination.iterator import search_auto_paging_iter as _paging_iter


class MerchantOrder(MPBase):
    """Groups payments into a single merchant-level order.

    Merchant orders are typically created automatically by Checkout Pro
    preferences but can also be managed manually to attach additional
    payments or shipments.
    """

    def search(self, filters=None, request_options=None):
        """Searches merchant orders matching the given filters.

        Args:
            filters: Query-string parameters (e.g. ``external_reference``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching merchant orders.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-pro/merchant_orders/search-merchant-order/get
        """
        return self._get(uri="/merchant_orders/search", filters=filters,
                         request_options=request_options)

    def get(self, merchant_order_id=None, request_options=None, **kwargs):
        """Retrieves a merchant order by its ID.

        Args:
            merchant_order_id: Unique merchant order identifier.
            request_options: Per-call configuration overrides.
            **kwargs: Supports the deprecated ``merchan_order_id`` spelling.

        Returns:
            dict: Full merchant order object including attached payments.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-pro/merchant_orders/get-merchant-order/get
        """
        merchant_order_id = self._resolve_merchant_order_id(
            merchant_order_id, kwargs)
        return self._get(uri="/merchant_orders/" + self._path_param(merchant_order_id),
                         request_options=request_options)

    def update(self, merchant_order_id=None, merchant_order_object=None,
               request_options=None, **kwargs):
        """Updates an existing merchant order.

        Args:
            merchant_order_id: Identifier of the merchant order to update.
            merchant_order_object: Dict with the fields to modify.
            request_options: Per-call configuration overrides.
            **kwargs: Supports the deprecated ``merchan_order_id`` spelling.

        Raises:
            ValueError: If *merchant_order_object* is not a ``dict``.

        Returns:
            dict: Updated merchant order object.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-pro/merchant_orders/update-merchant-order/put
        """
        merchant_order_id = self._resolve_merchant_order_id(
            merchant_order_id, kwargs)
        if not isinstance(merchant_order_object, dict):
            raise ValueError(
                "Param merchant_order_object must be a Dictionary")

        return self._put(uri="/merchant_orders/" + self._path_param(merchant_order_id),
                         data=merchant_order_object, request_options=request_options)

    @staticmethod
    def _resolve_merchant_order_id(merchant_order_id, kwargs):
        """Resolves the corrected ID keyword and its legacy misspelling."""
        missing = object()
        legacy_id = kwargs.pop("merchan_order_id", missing)
        if kwargs:
            unexpected = next(iter(kwargs))
            raise TypeError("Unexpected keyword argument: " + unexpected)
        if merchant_order_id is not None and legacy_id is not missing:
            raise TypeError(
                "Use either merchant_order_id or merchan_order_id, not both")
        merchant_order_id = (
            merchant_order_id if legacy_id is missing else legacy_id
        )
        if merchant_order_id is None:
            raise TypeError("merchant_order_id is required")
        return merchant_order_id

    def create(self, merchant_order_object, request_options=None):
        """Creates a new merchant order.

        Args:
            merchant_order_object: Dict describing the order (items,
                preference_id, application_id, etc.).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *merchant_order_object* is not a ``dict``.

        Returns:
            dict: Created merchant order including its ``id``.

        Reference: https://www.mercadopago.com/developers/en/reference
        """
        if not isinstance(merchant_order_object, dict):
            raise ValueError(
                "Param merchant_order_object must be a Dictionary")

        return self._post(uri="/merchant_orders", data=merchant_order_object,
                          request_options=request_options)

    def create_instore_order(self, user_id, external_id, order_object,
                             request_options=None):
        """Creates a deprecated V1 in-store QR order.

        .. deprecated:: 3.6.0
           This compatibility operation maps to
           ``POST /mpmobile/instore/qr/{user_id}/{external_id}``.
        """
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._post(
            uri=("/mpmobile/instore/qr/" + self._path_param(user_id) + "/"
                 + self._path_param(external_id)),
            data=order_object,
            request_options=request_options,
        )

    def delete_instore_order(self, user_id, external_id, request_options=None):
        """Deletes a deprecated V1 in-store QR order."""
        return self._delete(
            uri=("/mpmobile/instore/qr/" + self._path_param(user_id) + "/"
                 + self._path_param(external_id)),
            request_options=request_options,
        )

    def create_instore_order_v2(self, user_id, external_store_id,
                                external_pos_id, order_object,
                                request_options=None):
        """Creates a deprecated V2 in-store QR order."""
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._put(
            uri=("/instore/qr/seller/collectors/" + self._path_param(user_id)
                 + "/stores/" + self._path_param(external_store_id) + "/pos/"
                 + self._path_param(external_pos_id) + "/orders"),
            data=order_object,
            request_options=request_options,
        )

    def get_instore_order_v2(self, user_id, external_pos_id,
                             request_options=None):
        """Retrieves a deprecated V2 in-store QR order."""
        return self._get(
            uri=("/instore/qr/seller/collectors/" + self._path_param(user_id)
                 + "/pos/" + self._path_param(external_pos_id) + "/orders"),
            request_options=request_options,
        )

    def delete_instore_order_v2(self, user_id, external_pos_id,
                                request_options=None):
        """Deletes a deprecated V2 in-store QR order."""
        return self._delete(
            uri=("/instore/qr/seller/collectors/" + self._path_param(user_id)
                 + "/pos/" + self._path_param(external_pos_id) + "/orders"),
            request_options=request_options,
        )

    def create_qr_tramma_dynamic(self, user_id, external_pos_id, qr_object,
                                 request_options=None):
        """Creates a deprecated dynamic QR trama."""
        if not isinstance(qr_object, dict):
            raise ValueError("Param qr_object must be a Dictionary")
        return self._post(
            uri=("/instore/orders/qr/seller/collectors/"
                 + self._path_param(user_id) + "/pos/"
                 + self._path_param(external_pos_id) + "/qrs"),
            data=qr_object,
            request_options=request_options,
        )

    def create_dynamic_qr_order(self, user_id, external_pos_id, order_object,
                                request_options=None):
        """Creates a deprecated dynamic QR order."""
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._put(
            uri=("/instore/orders/qr/seller/collectors/"
                 + self._path_param(user_id) + "/pos/"
                 + self._path_param(external_pos_id) + "/qrs"),
            data=order_object,
            request_options=request_options,
        )

    def search_auto_paging_iter(self, filters=None, request_options=None, limit=100):
        """Lazily yields all items matching *filters* across all pages."""
        return _paging_iter(self.search, filters, request_options, limit)
