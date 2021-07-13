import asyncio
import aiohttp

import base64

from datetime import datetime

from .base import BaseCaptcha
from .errors import (
    AlreadySolved,
    BadRequest,
    IncorrectCaptcha,
    TooManyTries,
    UUIDExpired,
)


class AsyncCaptcha(BaseCaptcha):
    """Same as `Captcha` in functionality but is Asynchronous"""

    def __init__(
        self,
        resp: dict,
        session: aiohttp.ClientSession = None,
        close_session_after_verify = False,
        base_url: str = None,
        generate_endpoint: str = None,
        verify_endpoint: str = None,
    ) -> None:
        """Returns a new instance of `AsyncCaptcha`
        
        You should get this using `Captcha.new` instead of manually constructing.
        """

        self.session = session or aiohttp.ClientSession()
        self.close_session_after_verify = close_session_after_verify

        self.base_url = base_url or self.API_BASE_URL
        self.generate_endpoint = generate_endpoint or self.GENERATE_ENDPOINT
        self.verify_endpoint = verify_endpoint or self.VERIFY_ENDPOINT

        self.uuid = resp["uuid"]
        self.timestamp = datetime.strptime(resp["ts"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.captcha = resp["captcha"][
            22:
        ]  # remove data type in the beginning of response

    @staticmethod
    async def _generate(session: aiohttp.ClientSession, params: dict, base_url: str, generate_endpoint: str) -> dict:
        """Sends a GET request to the generate endpoint

        Args:
            session (aiohttp.ClientSession) the client session to use
            params (dict): the url params
            base_url (str): the API base URL
            generate_endpoint (str): the API endpoint for generating captcha

        Returns:
            dict: returns json response
        """

        params = {k:v for (k, v) in params.items() if v} # To remove None values

        async with session.get(f"{base_url}{generate_endpoint}", params=params) as resp:
            return await resp.json()

    @staticmethod
    async def _verify(
        session: aiohttp.ClientSession, base_url: str, verify_endpoint: str, uuid: str, text: str
    ) -> aiohttp.ClientResponse:
        """Sends a POST request to the verify endpoint

        Args:
            session (aiohttp.ClientSession): the client session to use
            base_url (str): the API base URL
            verify_endpoint (str): the API endpoint for verifying a captcha
            uuid (str): the captcha's unique identifier
            text (str): the user response to be verified

        Returns:
            requests.Response: requests `Response` object
        """

        return await session.post(
            f"{base_url}{verify_endpoint}", json={"uuid": uuid, "captcha": text}
        )
    
    @classmethod
    async def new(
        cls,
        session: aiohttp.ClientSession=None,
        close_session_after_verify=False,
        height: int = None,
        width: int = None,
        circles: int = None,
        length: int = None,
        base_url: str = None,
        generate_endpoint: str = None,
        verify_endpoint: str = None,
    ):
        """Generates a new Captcha asynchronously

        Args:
            session (aiohttp.ClientSession, optional): The AioHTTP `ClientSession` to reuse. Creates a new one if not given.
            close_session_after_verify (bool, optional): Should close client session after verification or not. Defaults to `False`.
            height (int, optional): Height of the Captcha generated (max 250). Defaults to None.
            width (int, optional): Width of the Captcha generated (max 500). Defaults to None.
            circles (int, optional): Number of circles in Captcha generated (max 150). Defaults to None.
            length (int, optional): Number of characters in Captcha generated (max 10). Defaults to None.
            base_url (str, optional): API base URL. Defaults to "https://captcha-api.akshit.me/v2".
            generate_endpoint (str, optional): API endpoint for generate. Defaults to "/generate".
            verify_endpoint (str, optional): API endpoint for verify. Defaults to "/verify".

        Returns a new instance of `Captcha`
        """

        session = session or aiohttp.ClientSession()
        json = await cls._generate(
            session,
            {"height": height, "width": width, "circles": circles, "length": length},
            base_url or cls.API_BASE_URL,
            generate_endpoint or cls.GENERATE_ENDPOINT,
        )

        return cls(
            json,
            session,
            close_session_after_verify=close_session_after_verify,
            base_url=base_url,
            generate_endpoint=generate_endpoint,
            verify_endpoint=verify_endpoint,
        )

    async def decode(self) -> bytes:
        """Decodes a Captcha into `bytes`

        Decodes in an async executor unlike sync decode to prevent blocking.

        Returns:
            bytes: Captcha decoded as bytes
        """

        loop = asyncio.get_event_loop()

        self.captcha_decoded = await loop.run_in_executor(None, base64.b64decode, self.captcha)

        return self.captcha_decoded

    async def verify(self, text: str) -> bool:
        """Verifies the Captcha instance with user input

        Args:
            text (str): the text to be verified

        Raises:
            BadRequest: If status code 400 is recieved by the API
            IncorrectCaptcha: If the user input is faulty (401)
            UUIDExpired: If UUID associated with the Captcha expires (404)
            AlreadySolved: If the Captcha has already been solved (409)
            TooManyTries: If a Captcha has been tried many times (429)

        Returns:
            bool: returns `True` upon successful verification
        """

        resp = await self._verify(self.session, self.base_url, self.verify_endpoint, self.uuid, text)
        json = await resp.json()

        if self.close_session_after_verify:
            await self.session.close()

        if resp.status == 200:
            return True

        if resp.status == 400:
            raise BadRequest(json, 400)

        if resp.status == 401:
            raise IncorrectCaptcha(json, 401)

        if resp.status == 404:
            raise UUIDExpired(json, 404)

        if resp.status == 409:
            raise AlreadySolved(json, 409)

        if resp.status == 429:
            raise TooManyTries(json, 429)
