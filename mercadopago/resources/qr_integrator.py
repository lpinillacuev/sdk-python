"""QR integrator configuration resource for in-store payments."""

from json.encoder import JSONEncoder

from mercadopago.core import MPBase
from mercadopago.errors.response import MPResponse


class QRIntegrator(MPBase):
    """Manage the authenticated seller's QR integrator configuration."""

    def get_qr_integrator_config(self, request_options=None):
        """Retrieve the QR integrator configuration, including callback_url."""
        return self._get(uri="/instore/integrator", request_options=request_options)

    def create_qr_integrator_config(self, data, request_options=None):
        """Create or update the configuration with a JSON callback_url payload.

        The payload may also contain the optional notification_url.
        """
        if data is not None:
            data = JSONEncoder().encode(data)

        if request_options is not None and not isinstance(request_options, type(self.request_options)):
            raise ValueError("Param request_options must be a RequestOptions Object")
        if request_options is None:
            request_options = self.request_options
        if request_options.access_token is None:
            request_options.access_token = self.request_options.access_token

        headers = request_options.get_headers()
        headers.update({"Content-type": self.config.mime_json})
        return MPResponse(self._QRIntegrator__http_patch(
            data=data, headers=headers, request_options=request_options,
        ))

    def __http_patch(self, data, headers, request_options):
        """Send PATCH through the configured HTTP client's generic request method."""
        return self._MPBase__http_client.request(
            "PATCH",
            url=self.config.api_base_url + "/instore/integrator",
            data=data,
            params=None,
            headers=headers,
            timeout=request_options.connection_timeout,
            maxretries=request_options.max_retries,
            retry_on=request_options.retry_on,
        )