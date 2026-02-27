"""DataUpdateCoordinator for BIR Trash."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from birtrashclient import BirTrashAuthError, BirTrashClient, BirTrashConnectionError

from .const import (
    CONF_ADDRESS_ID,
    CONF_APP_ID,
    CONF_CONTRACTOR_ID,
    DOMAIN,
    FETCH_DAYS,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class BirTrashCoordinator(DataUpdateCoordinator[list[dict[str, Any]]]):
    """Coordinator to fetch BIR Trash pickup data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        session = async_get_clientsession(hass)
        self.client = BirTrashClient(
            app_id=entry.data[CONF_APP_ID],
            contractor_id=entry.data[CONF_CONTRACTOR_ID],
            session=session,
        )
        self.address_id: str = entry.data[CONF_ADDRESS_ID]

    async def _async_update_data(self) -> list[dict[str, Any]]:
        """Fetch pickup calendar from BIR API."""
        try:
            await self.client.authenticate()
            from_date = date.today().isoformat()
            to_date = (date.today() + timedelta(days=FETCH_DAYS)).isoformat()
            return await self.client.get_calendar(self.address_id, from_date, to_date)
        except BirTrashAuthError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except BirTrashConnectionError as err:
            raise UpdateFailed(f"Connection error: {err}") from err
