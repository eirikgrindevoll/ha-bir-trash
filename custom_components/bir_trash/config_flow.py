"""Config flow for BIR Trash integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from birtrashclient import BirTrashAuthError, BirTrashClient, BirTrashConnectionError

from .const import (
    CONF_ADDRESS,
    CONF_ADDRESS_ID,
    CONF_APP_ID,
    CONF_CONTRACTOR_ID,
    DEFAULT_APP_ID,
    DEFAULT_CONTRACTOR_ID,
    DOMAIN,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_APP_ID, default=DEFAULT_APP_ID): str,
        vol.Required(CONF_CONTRACTOR_ID, default=DEFAULT_CONTRACTOR_ID): str,
        vol.Required(CONF_ADDRESS): str,
    }
)


class BirTrashConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BIR Trash."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._app_id: str = ""
        self._contractor_id: str = ""
        self._addresses: list[dict] = []

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._app_id = user_input[CONF_APP_ID]
            self._contractor_id = user_input[CONF_CONTRACTOR_ID]
            address_query = user_input[CONF_ADDRESS]

            session = async_get_clientsession(self.hass)
            client = BirTrashClient(
                app_id=self._app_id,
                contractor_id=self._contractor_id,
                session=session,
            )

            try:
                await client.authenticate()
                addresses = await client.search_addresses(address_query)
            except BirTrashAuthError:
                errors["base"] = "invalid_auth"
            except BirTrashConnectionError:
                errors["base"] = "cannot_connect"
            else:
                if not addresses:
                    errors["base"] = "no_addresses_found"
                elif len(addresses) == 1:
                    address = addresses[0]
                    await self.async_set_unique_id(address["id"])
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title=address["adresse"],
                        data={
                            CONF_APP_ID: self._app_id,
                            CONF_CONTRACTOR_ID: self._contractor_id,
                            CONF_ADDRESS_ID: address["id"],
                            CONF_ADDRESS: address["adresse"],
                        },
                    )
                else:
                    self._addresses = addresses
                    return await self.async_step_select_address()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_select_address(self, user_input=None):
        """Handle address selection when multiple addresses are found."""
        errors: dict[str, str] = {}

        if user_input is not None:
            selected_adresse = user_input[CONF_ADDRESS]
            selected = next(
                a for a in self._addresses if a["adresse"] == selected_adresse
            )
            await self.async_set_unique_id(selected["id"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=selected["adresse"],
                data={
                    CONF_APP_ID: self._app_id,
                    CONF_CONTRACTOR_ID: self._contractor_id,
                    CONF_ADDRESS_ID: selected["id"],
                    CONF_ADDRESS: selected["adresse"],
                },
            )

        options = [a["adresse"] for a in self._addresses]
        schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        mode=SelectSelectorMode.LIST,
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="select_address",
            data_schema=schema,
            errors=errors,
        )
