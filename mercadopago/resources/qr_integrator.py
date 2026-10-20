"""QR integrator configuration resource."""
from mercadopago.core import MPBase


class QRIntegrator(MPBase):
    """Manages QR integrator settings for in-store payments."""

    def create_qr_integrator_config(self, config_object, request_options=None):
        """Creates or updates QR integrator settings.

        Args:
            config_object: JSON body with callback_url and/or notification_url.
            request_options: Optional per-call request configuration.
        """
        if not isinstance(config_object, dict):
            raise ValueError("Param config_object must be a Dictionary")

        return self._patch(
            uri="/instore/integrator",
            data=config_object,
            request_options=request_options,
        )