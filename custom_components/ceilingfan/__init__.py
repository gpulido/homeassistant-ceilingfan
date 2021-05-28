"""Ceiling Fan Custom Component"""
from homeassistant import config_entries, core

from .const import DOMAIN



async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to the climate platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "fan")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "light")
    )
    return True



async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the homeassistant-ceilingfan component."""
    hass.data.setdefault(DOMAIN, {})
    # @TODO: Add setup code.
    return True
