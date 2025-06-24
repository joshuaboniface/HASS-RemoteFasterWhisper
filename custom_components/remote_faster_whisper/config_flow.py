import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigEntry

from . import DOMAIN

class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None, errors=None):
        if user_input:
            return self.async_create_entry(title="Remote Faster Whisper", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("uri", default=""): str,
                    vol.Required("language", default="en"): str,
                    vol.Required("result_prefix", default=""): str,
                },
            ),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration."""
        config_entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        
        if user_input is not None:
            # Update the config entry with new data
            self.hass.config_entries.async_update_entry(
                config_entry, data=user_input
            )
            await self.hass.config_entries.async_reload(config_entry.entry_id)
            return self.async_abort(reason="reconfigure_successful")

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required("uri", default=config_entry.data.get("uri", "")): str,
                    vol.Required("language", default=config_entry.data.get("language", "en")): str,
                    vol.Required("result_prefix", default=config_entry.data.get("result_prefix", "")): str,
                },
            ),
        )
