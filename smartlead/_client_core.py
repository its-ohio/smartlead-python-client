import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, Literal

from requests import Request, Session, Response, HTTPError

from ._utils import SMARTLEAD_API_URL, APIException, Json


__all__ = [
    "CoreClient",
]


class CoreClient:
    """
    Base class for smartlead client.
    """

    # 10 requests very 2 seconds: https://help.smartlead.ai/API-Documentation-a0d223bdd3154a77b3735497aad9419f
    # it's not documented (as far as I know), but there seems to be an additional limit of 60 requests per minute :(
    _REQUEST_WAIT_TIME = 1

    def __init__(self, api_key: str) -> None:
        if not isinstance(api_key, str):
            raise ValueError(
                f"API-key must be a string, can't be of type {type(api_key).__name__}."
            )

        self._api_key = api_key
        self._session = Session()
        # to avoid rate limiting:
        self._last_request_time = 0.0
        self._rate_limit_lock = threading.Lock()

    def _make_request(
        self,
        request_type: Literal["GET", "POST", "DELETE"],
        endpoint: str,
        params: Optional[Dict[str, Json]] = None,
        data: Optional[Dict[str, Json]] = None,
        allow_text_return: bool = False,
    ) -> dict | list | str:
        # format parameters:
        parameters: dict = {} if params is None else params
        parameters["api_key"] = self._api_key
        parameters = {key: val for key, val in parameters.items() if val is not None}

        request = Request(
            method=request_type,
            url=f"{SMARTLEAD_API_URL}/{endpoint}",
            params=parameters,
            data=data,
        )
        with ThreadPoolExecutor() as executor:
            # rate limit wait:
            with self._rate_limit_lock:
                # TODO: Implement stack rate-limiting (faster!)
                time_since_request = time.time() - self._last_request_time
                wait_time = self._REQUEST_WAIT_TIME - time_since_request
                if wait_time > 1:
                    time.sleep(wait_time)
                else:
                    time.sleep(1)

                # submit future and set timer:
                future = executor.submit(  # noqa
                    self._session.send,
                    request.prepare(),
                )
                self._last_request_time = time.time()

        response: Response = future.result()
        # check for errors:
        try:
            response.raise_for_status()

        except HTTPError:
            raise APIException(response.text)

        # sometimes we get a csv returned:
        try:
            return response.json()

        except json.JSONDecodeError:
            # there is one endpoint which returns data in a csv-type string:
            if allow_text_return:
                return response.text

            raise

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Json]] = None,
        allow_text_return: bool = False,
    ) -> dict | list | str:
        return self._make_request(
            request_type="GET",
            endpoint=endpoint,
            params=params,
            allow_text_return=allow_text_return,
        )

    def _post(
        self,
        endpoint: str,
        params: Optional[Dict[str, Json]] = None,
        data: Optional[Dict[str, Json]] = None,
    ) -> dict:
        return self._make_request(
            request_type="POST",
            endpoint=endpoint,
            params=params,
            data=data,
        )

    def _delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Json]] = None,
        data: Optional[Dict[str, Json]] = None,
    ) -> dict:
        return self._make_request(
            request_type="DELETE",
            endpoint=endpoint,
            params=params,
            data=data,
        )
