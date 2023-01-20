from typing import Any

from pyckish.event_elements.event_element import EventElement


class HTTPHeaders(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Headers
    """
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def extract(event: dict, context: dict) -> Any:
        try:
            argument = event['headers']
        except KeyError:
            argument = {}
        return argument
