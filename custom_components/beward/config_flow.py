"""Adds config flow for Beward."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.ffmpeg.camera import DEFAULT_ARGUMENTS
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, \
    CONF_PASSWORD, CONF_NAME

from .camera import CAMERAS
from .const import DOMAIN, CONF_RTSP_PORT, CONF_STREAM, \
    CONF_FFMPEG_ARGUMENTS, CONF_CAMERAS, DATA_BEWARD


@config_entries.HANDLERS.register(DOMAIN)
class BewardFlowHandler(config_entries.ConfigFlow):
    """Config flow for Beward."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    _hassio_discovery = None

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_import(self,
                                user_input):  # pylint: disable=unused-argument
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})

    async def _show_setup_form(self, user_input):
        """Show the configuration form to edit location data."""

        if user_input is None:
            user_input = {}

        name = user_input.get(CONF_NAME, '')
        host = user_input.get(CONF_HOST, '')
        port = user_input.get(CONF_PORT, 80)
        username = user_input.get(CONF_USERNAME, '')
        password = user_input.get(CONF_PASSWORD, '')
        rtsp_port = user_input.get(CONF_RTSP_PORT, 554)
        stream = user_input.get(CONF_STREAM, 0)
        ffmpeg_arg = user_input.get(CONF_FFMPEG_ARGUMENTS, DEFAULT_ARGUMENTS)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=host): str,
                vol.Required(CONF_USERNAME, default=username): str,
                vol.Required(CONF_PASSWORD, default=password): str,
                # vol.Required(CONF_CAMERAS, default=list(CAMERAS)):
                #     vol.All(cv.ensure_list, [vol.In(CAMERAS)]),
                vol.Optional(CONF_PORT, default=port): vol.Coerce(int),
                vol.Optional(CONF_NAME, default=name): str,
                vol.Optional(CONF_RTSP_PORT, default=rtsp_port): int,
                vol.Optional(CONF_STREAM, default=stream): int,
                vol.Optional(CONF_FFMPEG_ARGUMENTS, default=ffmpeg_arg): str,
            }), errors=self._errors,
        )

    async def async_step_user(
            self, user_input={}
    ):  # pylint: disable=dangerous-default-value
        """Handle a flow initialized by the user."""
        self._errors = {}

        # return self.async_abort(reason="in_development")

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DATA_BEWARD):
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input["username"], user_input["password"]
            )
            if valid:
                return self.async_create_entry(title="", data=user_input)

            self._errors["base"] = "auth"
            return await self._show_setup_form(user_input)

        return await self._show_setup_form(user_input)

    async def _test_credentials(self, username, password):
        """Return true if credentials is valid."""
        try:
            # client = Client(username, password)
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False

    async def async_step_ssdp(self, info):  # pylint: disable=unused-argument
        """Handle a flow initialized by SSDP/UPNP."""
        self._errors = {}

        return self.async_abort(reason="in_development")
