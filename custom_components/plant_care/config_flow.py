"""Config flow for Plant Care integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_HUMIDITY_SENSOR,
    CONF_HUMIDITY_THRESHOLD,
    CONF_PLANT_NAME,
    DEFAULT_HUMIDITY_THRESHOLD,
    DOMAIN,
)


class PlantCareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Plant Care."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_PLANT_NAME].lower())
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_PLANT_NAME],
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_PLANT_NAME): selector.TextSelector(),
                vol.Required(CONF_HUMIDITY_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(
                    CONF_HUMIDITY_THRESHOLD, default=DEFAULT_HUMIDITY_THRESHOLD
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=100, unit_of_measurement="%", mode="box"
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return PlantCareOptionsFlow()


class PlantCareOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Plant Care."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_HUMIDITY_SENSOR,
                    default=current.get(CONF_HUMIDITY_SENSOR),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(
                    CONF_HUMIDITY_THRESHOLD,
                    default=current.get(
                        CONF_HUMIDITY_THRESHOLD, DEFAULT_HUMIDITY_THRESHOLD
                    ),
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=100, unit_of_measurement="%", mode="box"
                    )
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)