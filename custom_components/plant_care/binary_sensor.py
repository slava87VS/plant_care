"""Binary sensor platform for Plant Care."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_HUMIDITY,
    ATTR_THRESHOLD,
    CONF_HUMIDITY_SENSOR,
    CONF_HUMIDITY_THRESHOLD,
    DEFAULT_HUMIDITY_THRESHOLD,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Plant Care binary sensor."""
    async_add_entities([PlantNeedsWaterBinarySensor(hass, entry)])


class PlantNeedsWaterBinarySensor(BinarySensorEntity):
    """Binary sensor: True if soil moisture is below threshold."""

    _attr_has_entity_name = True
    _attr_name = "Needs water"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:water-alert"
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.hass = hass
        self.entry = entry
        self._plant_name = entry.data.get("plant_name", "Plant")
        self._humidity_sensor = entry.data.get(CONF_HUMIDITY_SENSOR)
        self._attr_unique_id = f"{entry.entry_id}_needs_water"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": f"Plant: {self._plant_name}",
            "manufacturer": "Plant Care",
            "model": "Soil Moisture Monitor",
        }

    @property
    def _threshold(self) -> float:
        """Return configured humidity threshold."""
        return float(
            self.entry.options.get(
                CONF_HUMIDITY_THRESHOLD,
                self.entry.data.get(
                    CONF_HUMIDITY_THRESHOLD, DEFAULT_HUMIDITY_THRESHOLD
                ),
            )
        )

    @property
    def _humidity(self) -> float | None:
        """Read humidity sensor value."""
        if not self._humidity_sensor:
            return None
        state = self.hass.states.get(self._humidity_sensor)
        if state is None or state.state in ("unknown", "unavailable"):
            return None
        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None

    @property
    def is_on(self) -> bool:
        """Return True if plant needs water."""
        humidity = self._humidity
        if humidity is None:
            # No sensor / no data → assume OK to avoid false alarms
            return False
        return humidity < self._threshold

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        return {
            ATTR_HUMIDITY: self._humidity,
            ATTR_THRESHOLD: self._threshold,
            "humidity_sensor": self._humidity_sensor,
        }