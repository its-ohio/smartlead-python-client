import re
from typing import TypeAlias, Dict

__all__ = [
    "SMARTLEAD_API_URL",
    "Json",
    "JsonDict",
    "APIException",
    "compact_list_to_str",
]

SMARTLEAD_API_URL = "https://server.smartlead.ai/api/v1"


Json: TypeAlias = dict | list | str | int | bool | float
JsonDict: TypeAlias = Dict[str, Json]


class APIException(Exception):
    """
    Raised from smartlead API errors.
    """


def compact_list_to_str(obj: list) -> str:
    return str(obj).replace(" ", "")


def to_snake_case(_s: str) -> str:
    snake_case = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", _s)
    return snake_case.lower()
