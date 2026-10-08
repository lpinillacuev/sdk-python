"""Main entry point for the MercadoPago Python SDK.

Instantiate :class:`SDK` with an access token to obtain factory methods
for every MercadoPago API resource (payments, orders, customers, etc.).

Example::

    import mercadopago

    sdk = mercadopago.SDK("YOUR_ACCESS_TOKEN")
    result = sdk.payment().create({
        "transaction_amount": 100,
        "payment_method_id": "pix",
        "payer": {"email": "buyer@example.com"},
    })
"""
from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient
from mercadopago.resources import (
    AdvancedPayment,
    Card,
    CardToken,
    Chargeback,
    Claim,
    Customer,
    DisbursementRefund,
    IdentificationType,
    Invoice,
    MerchantOrder,
    OAuth,
    Order,
    Payment,
    PaymentMethods,
    Payout,
    Plan,
    Point,
    POS,
    PreApproval,
    Preference,
    Refund,
    ReleaseReport,
    SettlementReport,
    Store,
    Subscription,
    Terminals,
    User,
)


class SDK:  # pylint: disable=too-many-public-methods
    """Central client providing factory methods for every API resource."""

    def __init__(self, access_token, http_client=None, request_options=None):
        self.http_client = http_client
        if http_client is None:
            self.http_client = HttpClient()

        self.request_options = request_options
        if request_options is None:
            self.request_options = RequestOptions()

        self.request_options.access_token = access_token

    def advanced_payment(self, request_options=None):
        return AdvancedPayment(request_options is not None and request_options
                               or self.request_options, self.http_client)

    def card_token(self, request_options=None):
        return CardToken(request_options is not None and request_options
                         or self.request_options, self.http_client)

    def card(self, request_options=None):
        return Card(request_options is not None and request_options
                    or self.request_options, self.http_client)

    def customer(self, request_options=None):
        return Customer(request_options is not None and request_options
                        or self.request_options, self.http_client)

    def disbursement_refund(self, request_options=None):
        return DisbursementRefund(request_options is not None and request_options
                                  or self.request_options, self.http_client)

    def identification_type(self, request_options=None):
        return IdentificationType(request_options is not None and request_options
                                  or self.request_options, self.http_client)

    def invoice(self, request_options=None):
        return Invoice(request_options is not None and request_options
                       or self.request_options, self.http_client)

    def oauth(self, request_options=None):
        return OAuth(request_options is not None and request_options
                     or self.request_options, self.http_client)

    def point(self, request_options=None):
        return Point(request_options is not None and request_options
                     or self.request_options, self.http_client)

    def terminals(self, request_options=None):
        """Returns the resource for terminal setup, refunds, and actions."""
        options = request_options if request_options is not None else self.request_options
        return Terminals(options, self.http_client)

    def claim(self, request_options=None):
        return Claim(request_options is not None and request_options
                     or self.request_options, self.http_client)

    def payout(self, request_options=None):
        return Payout(request_options is not None and request_options
                      or self.request_options, self.http_client)

    def pos(self, request_options=None):
        return POS(request_options is not None and request_options
                   or self.request_options, self.http_client)

    def store(self, request_options=None):
        return Store(request_options is not None and request_options
                     or self.request_options, self.http_client)

    def merchant_order(self, request_options=None):
        return MerchantOrder(request_options is not None and request_options
                             or self.request_options, self.http_client)

    def order(self, request_options=None):
        return Order(request_options is not None and request_options
                     or self.request_options, self.http_client)

    def payment(self, request_options=None):
        return Payment(request_options is not None and request_options
                       or self.request_options, self.http_client)

    def payment_methods(self, request_options=None):
        return PaymentMethods(request_options is not None and request_options
                              or self.request_options, self.http_client)

    def preapproval(self, request_options=None):
        return PreApproval(request_options is not None and request_options
                           or self.request_options, self.http_client)

    def preference(self, request_options=None):
        return Preference(request_options is not None and request_options
                          or self.request_options, self.http_client)

    def refund(self, request_options=None):
        return Refund(request_options is not None and request_options
                      or self.request_options, self.http_client)

    def user(self, request_options=None):
        return User(request_options is not None and request_options
                    or self.request_options, self.http_client)

    def chargeback(self, request_options=None):
        return Chargeback(request_options is not None and request_options
                          or self.request_options, self.http_client)

    def subscription(self, request_options=None):
        return Subscription(request_options is not None and request_options
                            or self.request_options, self.http_client)

    def plan(self, request_options=None):
        return Plan(request_options is not None and request_options
                    or self.request_options, self.http_client)

    @property
    def request_options(self):
        return self.__request_options

    @request_options.setter
    def request_options(self, value):
        if value is not None and not isinstance(value, RequestOptions):
            raise ValueError(
                "Param request_options must be a RequestOptions Object")
        self.__request_options = value

    @property
    def http_client(self):
        return self.__http_client

    @http_client.setter
    def http_client(self, value):
        if value is not None and not isinstance(value, HttpClient):
            raise ValueError("Param http_client must be a HttpClient Object")
        self.__http_client = value