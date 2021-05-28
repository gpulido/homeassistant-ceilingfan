import logging
from typing import Any, Callable, Dict, List, Optional

from homeassistant import config_entries, core
from homeassistant.components.light import PLATFORM_SCHEMA, LightEntity
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
import voluptuous as vol
from voluptuous.validators import Boolean

from .ceiling_fan import *
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    }
)

def get_devices(config):
    server = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

    gateway = CeilingFanGateway(server, username, password)
    device = CeilingFanLight(gateway)
    _LOGGER.info("Ceiling Fan Light")
    return [device]

async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup fan from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    devices = get_devices(config)
    async_add_entities(devices)

def setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    devices = get_devices(config)
    add_entities(devices)


#TODO: refactor common features from light & fan
class CeilingFanLight(LightEntity):

    def __init__(self, gateway: CeilingFanGateway):
        self._gateway = gateway
        self._is_on = False
        self._name = "Ceiling Fan Light"


    """Representation of a Ceiling Fan light."""

    def turn_on(self):
        """Turn on the light."""
        self._gateway.turn_light()
        self._is_on = True

    def turn_off(self) -> None:
        """Turn off the light."""
        self._gateway.turn_light()
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
    
    @property
    def unique_id(self):
        return self._gateway.unique_id() + '_Light'
