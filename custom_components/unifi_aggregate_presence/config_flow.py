import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
    DEVICE_DEFAULT_NAME,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_FIXED_HOSTS,
    CONF_HOME_SUBNET,
    CONF_SITE_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


def _parse_fixed_hosts(raw_hosts: str) -> list[str]:
    return [host.strip() for host in raw_hosts.splitlines() if host.strip()]


class FlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            data = dict(user_input)
            data[CONF_FIXED_HOSTS] = _parse_fixed_hosts(data.get(CONF_FIXED_HOSTS, ""))
            return self.async_create_entry(title=data[CONF_NAME], data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=DEVICE_DEFAULT_NAME): str,
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_SITE_ID, default="default"): str,
                    vol.Required(CONF_HOME_SUBNET): str,
                    vol.Optional(CONF_FIXED_HOSTS, default=""): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.Coerce(int),
                }
            ),
            errors={},
        )
