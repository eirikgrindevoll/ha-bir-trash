"""Constants for the BIR Trash integration."""

from datetime import timedelta

DOMAIN = "bir_trash"

CONF_APP_ID = "app_id"
CONF_CONTRACTOR_ID = "contractor_id"
CONF_ADDRESS_ID = "address_id"
CONF_ADDRESS = "address"

DEFAULT_APP_ID = "94FA72AD-583D-4AA3-988F-491F694DFB7B"
DEFAULT_CONTRACTOR_ID = "100;300;400"

SCAN_INTERVAL = timedelta(hours=12)
FETCH_DAYS = 30
