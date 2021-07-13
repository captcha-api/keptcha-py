import requests

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


class Captcha(BaseCaptcha):
    """Main Captcha Object"""

    def __init__(
        self, resp: dict, base_url=None, generate_endpoint=None, verify_endpoint=None
    ) -> None:
        """Returns a new instance of `Captcha`
        
        You should get this using `Captcha.new` instead of manually constructing.
        """

        self.base_url = base_url or self.API_BASE_URL
        self.generate_endpoint = generate_endpoint or self.GENERATE_ENDPOINT
        self.verify_endpoint = verify_endpoint or self.VERIFY_ENDPOINT

        self.uuid = resp["uuid"]
        self.timestamp = datetime.strptime(resp["ts"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.captcha = resp["captcha"][
            22:
        ]  # remove data type in the beginning of response

    @staticmethod
    def _generate(params: dict, base_url: str, generate_endpoint: str) -> dict:
        """Sends a GET request to the generate endpoint

        Args:
            params (dict): the url params
            base_url (str): the API base URL
            generate_endpoint (str): the API endpoint for generating captcha

        Returns:
            dict: returns json response
        """
        resp = requests.get(f"{base_url}{generate_endpoint}", params=params)

        return resp.json()

    @staticmethod
    def _verify(
        base_url: str, verify_endpoint: str, uuid: str, text: str
    ) -> requests.Response:
        """Sends a POST request to the verify endpoint

        Args:
            base_url (str): the API base URL
            verify_endpoint (str): the API endpoint for verifying a captcha
            uuid (str): the captcha's unique identifier
            text (str): the user response to be verified

        Returns:
            requests.Response: requests `Response` object
        """
        return requests.post(
            f"{base_url}{verify_endpoint}", json={"uuid": uuid, "captcha": text}
        )

    @classmethod
    def new(
        cls,
        height: int = None,
        width: int = None,
        circles: int = None,
        length: int = None,
        base_url: str = None,
        generate_endpoint: str = None,
        verify_endpoint: str = None,
    ):
        """Generates a new CAPTCHA

        Args:
            height (int, optional): Height of the Captcha generated (max 250). Defaults to None.
            width (int, optional): Width of the Captcha generated (max 500). Defaults to None.
            circles (int, optional): Number of circles in Captcha generated (max 150). Defaults to None.
            length (int, optional): Number of characters in Captcha generated (max 10). Defaults to None.
            base_url (str, optional): API base URL. Defaults to "https://captcha-api.akshit.me/v2".
            generate_endpoint (str, optional): API endpoint for generate. Defaults to "/generate".
            verify_endpoint (str, optional): API endpoint for verify. Defaults to "/verify".

        Returns a new instance of `Captcha`
        """
        json = cls._generate(
            {"height": height, "width": width, "circles": circles, "length": length},
            base_url or cls.API_BASE_URL,
            generate_endpoint or cls.GENERATE_ENDPOINT,
        )

        return cls(
            json,
            base_url=base_url,
            generate_endpoint=generate_endpoint,
            verify_endpoint=verify_endpoint,
        )

    def decode(self) -> bytes:
        """Decodes a Captcha into `bytes`

        Returns:
            bytes: Captcha decoded as bytes
        """
        self.captcha_decoded = base64.b64decode(self.captcha)

        return self.captcha_decoded

    def verify(self, text: str) -> bool:
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

        resp = self._verify(self.base_url, self.verify_endpoint, self.uuid, text)

        if resp.status_code == 200:
            return True

        if resp.status_code == 400:
            raise BadRequest(resp.json(), 400)

        if resp.status_code == 401:
            raise IncorrectCaptcha(resp.json(), 401)

        if resp.status_code == 404:
            raise UUIDExpired(resp.json(), 404)

        if resp.status_code == 409:
            raise AlreadySolved(resp.json(), 409)

        if resp.status_code == 429:
            raise TooManyTries(resp.json(), 429)
