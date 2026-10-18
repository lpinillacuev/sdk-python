"""QR Integrator configuration resource for in-store payments.

Wraps GET and PATCH /instore/integrator.
"""
from mercadopago.core import MPBase


class QRIntegrator(MPBase):
    """Gets and configures the authenticated account's QR integration."""

    def get(self, request_options=None):
        """Retrieve the QR integrator configuration.

        The returned response contains ``callback_url`` when configured.
        """
        return self._get(uri="/instore/integrator", request_options=request_options)

    def create(self, qr_integrator_object, request_options=None):
        """Create or update the QR integrator configuration via PATCH.

        ``callback_url`` and the deprecated ``notification_url`` are body
        properties, not URL query parameters.

        Args:
            qr_integrator_object: Configuration dictionary to send as JSON.
            request_options: Optional per-call configuration overrides.

        Raises:
            ValueError: If *qr_integrator_object* is not a dictionary.
        """
        if not isinstance(qr_integrator_object, dict):
            raise ValueError("Param qr_integrator_object must be a Dictionary")

        return self._patch(
            uri="/instore/integrator",
            data=qr_integrator_object,
            request_options=request_options,
        )