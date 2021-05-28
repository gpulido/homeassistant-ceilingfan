import logging
from typing import Any, Callable, Dict, List, Optional

from homeassistant import config_entries, core
from homeassistant.components.fan import (
    PLATFORM_SCHEMA,
    SUPPORT_DIRECTION,
    SUPPORT_SET_SPEED,
    FanEntity,
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
)
import voluptuous as vol

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
    device = CeilingFan(gateway)
    _LOGGER.info("Ceiling Fan")
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



ORDERED_NAMED_FAN_SPEEDS = ["1", "2", "3", "4", "5", "6"]  # off is not included


class CeilingFan(FanEntity):

    def __init__(self, gateway: CeilingFanGateway):
        self._gateway = gateway
        self._last_speed = ORDERED_NAMED_FAN_SPEEDS[0]
        self._direction = "forward"
        self._is_on = False
        self._name = "Ceiling Fan"

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off."""
        self._gateway.stop_fan()
        self._is_on = False

    def set_direction(self, direction: str) -> None:
        """Set the direction of the fan."""
        self._gateway.reverse_fan()
        self._direction = direction


    def turn_on(self, speed: Optional[str] = None, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
        if percentage is not None:
            self.set_percentage(percentage)
            return
        self.set_percentage(int(self._last_speed))


    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        speed = int(percentage_to_ordered_list_item(ORDERED_NAMED_FAN_SPEEDS, percentage))
        self._gateway.set_fan_speed(speed)
        self._last_speed = speed
        self._is_on = True

    @property
    def percentage(self) -> Optional[int]:
        """Return the current speed percentage."""
        return ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, str(self._last_speed))

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(ORDERED_NAMED_FAN_SPEEDS)

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_DIRECTION | SUPPORT_SET_SPEED

    @property
    def is_on(self):
        return self._is_on
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
    
    @property
    def unique_id(self):
        return self._gateway.unique_id() + '_Fan'
