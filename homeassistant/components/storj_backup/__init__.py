"""The storj_integration integration."""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import instance_id
from homeassistant.util.hass_dict import HassKey

from .api import StorjClient
from .const import DOMAIN

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type StorjConfigEntry = ConfigEntry[StorjClient]

DATA_BACKUP_AGENT_LISTENERS: HassKey[list[Callable[[], None]]] = HassKey(
    f"{DOMAIN}.backup_agent_listeners"
)


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: StorjConfigEntry) -> bool:
    """Set up storj_integration from a config entry."""

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

    entry.runtime_data = StorjClient(await instance_id.async_get(hass))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: StorjConfigEntry) -> bool:
    """Unload a config entry."""
    hass.loop.call_soon(_notify_backup_listeners, hass)
    return True


def _notify_backup_listeners(hass: HomeAssistant) -> None:
    for listener in hass.data.get(DATA_BACKUP_AGENT_LISTENERS, []):
        listener()
