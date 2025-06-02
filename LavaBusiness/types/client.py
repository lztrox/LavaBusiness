import aiohttp
from os import getenv
from .errors import LavaError

class AsyncClient:
    base_url: str
    client: aiohttp.ClientSession

    def __init__(self):
        self.base_url = getenv('LAVA_DSN') or 'https://api.lava.ru/business/'
        self._build_client()

    def _build_client(self):
        self.client = aiohttp.ClientSession(base_url=self.base_url)

    @staticmethod
    def _process_response(response: aiohttp.ClientResponse):
        if 200 <= response.status < 300:
            return response.json()
        else:
            raise LavaError(response.content)

    async def get(self, url: str, headers: dict) -> aiohttp.ClientResponse:
        return self._process_response(await self.client.get(url=url, headers=headers))

    async def post(self, url: str, json: dict, headers: dict) -> aiohttp.ClientResponse:
        return self._process_response(await self.client.post(url=url, json=json, headers=headers))