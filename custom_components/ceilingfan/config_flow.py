import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.const import (        
    CONF_HOST,    
    CONF_USERNAME,    
    CONF_PASSWORD,    
)
import homeassistant.helpers.config_validation as cv

import voluptuous as vol

from .const import  DOMAIN

_LOGGER = logging.getLogger(__name__)

CEILING_FAN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
     
    }
)

class AirzoneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Github Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:

            from .ceiling_fan import CeilingFanGateway
            server = user_input[CONF_HOST]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]  
            try:
                CeilingFanGateway(server, username, password)                
            except:
                errors["base"] = "connection"
            if not errors:
                self.data = user_input

                return self.async_create_entry(title="CeilingFan", data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=CEILING_FAN_SCHEMA, errors=errors
        )