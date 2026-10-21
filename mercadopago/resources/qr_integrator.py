"""QR integrator configuration resource for the Mercado Pago API."""
from mercadopago.core import MPBase


class QRIntegrator(MPBase):
    """Provides access to the QR integrator configuration."""

    def create_qr_integrator_config(self, data, request_options=None):
        """Creates or updates the QR integrator configuration.

        Args:
            data: Configuration containing ``callback_url`` and optionally
                deprecated ``notification_url``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated integrator configuration.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")

        return self._patch(
            uri="/instore/integrator",
            data=data,
            request_options=request_options,
        )

    def get_qr_integrator_config(self, request_options=None):
        """Retrieves the authenticated QR integrator configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Integrator configuration, including ``callback_url``.
        """
        return self._get(
            uri="/instore/integrator",
            request_options=request_options,
        )