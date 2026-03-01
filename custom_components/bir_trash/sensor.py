"""BIR Trash sensor platform."""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_ADDRESS, CONF_ADDRESS_ID, DOMAIN
from .coordinator import BirTrashCoordinator

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BIR Trash sensors from a config entry."""
    coordinator: BirTrashCoordinator = entry.runtime_data
    address_id = entry.data[CONF_ADDRESS_ID]
    address = entry.data[CONF_ADDRESS]

    known_fractions: set[str] = set()

    def _add_new_fraction_sensors() -> None:
        """Create sensors for any fractions not yet tracked."""
        new_entities = []
        for item in coordinator.data or []:
            fid = item["fraksjonId"]
            if fid not in known_fractions:
                known_fractions.add(fid)
                new_entities.append(
                    BirTrashSensor(
                        coordinator, address_id, address, fid, item["fraksjon"]
                    )
                )
        if new_entities:
            async_add_entities(new_entities)

    # Create sensors for fractions present now, and re-check on every update
    # so fractions added later by BIR automatically get a sensor.
    _add_new_fraction_sensors()
    entry.async_on_unload(coordinator.async_add_listener(_add_new_fraction_sensors))


class BirTrashSensor(CoordinatorEntity[BirTrashCoordinator], SensorEntity):
    """Sensor representing a single BIR waste fraction."""

    _attr_device_class = SensorDeviceClass.DATE
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: BirTrashCoordinator,
        address_id: str,
        address: str,
        fraction_id: str,
        fraction_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._address_id = address_id
        self._fraction_id = fraction_id
        self._attr_unique_id = f"{address_id}_{fraction_id}"
        self._attr_name = fraction_name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, address_id)},
            name=address,
            manufacturer="BIR",
        )

    def _sorted_dates(self) -> list[str]:
        """Return sorted ISO date strings for this fraction."""
        dates = [
            item["dato"].split("T")[0]
            for item in (self.coordinator.data or [])
            if item["fraksjonId"] == self._fraction_id
        ]
        dates.sort()
        return dates

    @property
    def native_value(self) -> date | None:
        """Return the next pickup date."""
        dates = self._sorted_dates()
        return date.fromisoformat(dates[0]) if dates else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return all upcoming pickup dates for this fraction."""
        return {"upcoming_dates": self._sorted_dates()}
