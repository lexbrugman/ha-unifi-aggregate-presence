import aiohttp

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=8)


class UnifiClient:
    def __init__(self, session: aiohttp.ClientSession, host: str, api_key: str, site_id: str):
        self._session = session
        self._host = host
        self._api_key = api_key
        self._site_id = site_id

    async def get_wireless_clients(self):
        url = f"https://{self._host}/proxy/network/api/s/{self._site_id}/stat/sta"
        headers = {"X-API-KEY": self._api_key}
        async with self._session.get(url, headers=headers, timeout=DEFAULT_TIMEOUT) as resp:
            resp.raise_for_status()
            data = await resp.json()
        return [c for c in data.get("data", []) if not c.get("is_wired", True)]
