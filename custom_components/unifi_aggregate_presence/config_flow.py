import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
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

    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> "OptionsFlowHandler":
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None) -> FlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            data = dict(user_input)
            data[CONF_FIXED_HOSTS] = _parse_fixed_hosts(data.get(CONF_FIXED_HOSTS, ""))
            return self.async_create_entry(title=data[CONF_NAME], data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=_build_data_schema(),
            errors={},
        )


def _build_data_schema(
    config: dict | None = None,
) -> vol.Schema:
    config = config or {}

    schema: dict = {
        vol.Optional(CONF_NAME, default=config.get(CONF_NAME, DEVICE_DEFAULT_NAME)): str,
        vol.Required(CONF_HOST, default=config.get(CONF_HOST, "")): str,
    }

    schema[vol.Required(CONF_USERNAME, default=config.get(CONF_USERNAME, ""))] = str
    schema[vol.Required(CONF_PASSWORD, default=config.get(CONF_PASSWORD, ""))] = str

    schema.update(
        {
            vol.Required(CONF_SITE_ID, default=config.get(CONF_SITE_ID, "default")): str,
            vol.Required(CONF_HOME_SUBNET, default=config.get(CONF_HOME_SUBNET, "")): str,
            vol.Optional(
                CONF_FIXED_HOSTS,
                default="\n".join(config.get(CONF_FIXED_HOSTS, [])),
            ): selector.TextSelector(selector.TextSelectorConfig(multiline=True)),
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ): vol.Coerce(int),
        }
    )

    return vol.Schema(schema)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            data = dict(user_input)
            data[CONF_FIXED_HOSTS] = _parse_fixed_hosts(data.get(CONF_FIXED_HOSTS, ""))
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data={
                    **self.config_entry.data,
                    **data,
                },
            )
            return self.async_create_entry(title="", data={})

        current_config = {
            **self.config_entry.data,
            **self.config_entry.options,
        }

        return self.async_show_form(
            step_id="init",
            data_schema=_build_data_schema(current_config),
            errors={},
        )
