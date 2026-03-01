"""BIR Trash calendar platform."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_ADDRESS, CONF_ADDRESS_ID, DOMAIN
from .coordinator import BirTrashCoordinator

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BIR Trash calendar from a config entry."""
    coordinator: BirTrashCoordinator = entry.runtime_data
    address_id = entry.data[CONF_ADDRESS_ID]
    address = entry.data[CONF_ADDRESS]
    async_add_entities([BirTrashCalendar(coordinator, address_id, address)])


class BirTrashCalendar(CoordinatorEntity[BirTrashCoordinator], CalendarEntity):
    """Calendar showing all BIR waste fraction pickups."""

    _attr_has_entity_name = True
    _attr_name = "Pickup schedule"

    def __init__(
        self,
        coordinator: BirTrashCoordinator,
        address_id: str,
        address: str,
    ) -> None:
        """Initialize the calendar."""
        super().__init__(coordinator)
        self._address_id = address_id
        self._attr_unique_id = f"{address_id}_calendar"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, address_id)},
            name=address,
            manufacturer="BIR",
        )

    def _events_in_range(self, start: date, end: date) -> list[CalendarEvent]:
        """Return all pickup events within [start, end]."""
        events = []
        for item in self.coordinator.data or []:
            pickup_date = date.fromisoformat(item["dato"].split("T")[0])
            if start <= pickup_date <= end:
                events.append(
                    CalendarEvent(
                        start=pickup_date,
                        end=pickup_date + timedelta(days=1),
                        summary=item["fraksjon"],
                    )
                )
        events.sort(key=lambda e: e.start)
        return events

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming pickup event."""
        today = date.today()
        upcoming = self._events_in_range(today, today + timedelta(days=365))
        return upcoming[0] if upcoming else None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return all events in the requested date range."""
        return self._events_in_range(start_date.date(), end_date.date())
