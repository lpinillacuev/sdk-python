"""Dataclass for transaction security data in order requests."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderTransactionSecurity:
    """Transaction security settings for an order request.

    Nested under ``config.online.transaction_security`` (not at the request root).
    It is serialized by :func:`order_request_to_dict`, which recursively filters
    ``None`` fields before sending.

    Attributes:
        validation: Validation strategy applied to the transaction (e.g.
            ``"complete"``). Type: str.
        liability_shift: Liability shift indicator for 3-D Secure flows. Type: str.
    """

    validation: Optional[str] = None
    liability_shift: Optional[str] = None
