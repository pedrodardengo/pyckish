from typing import Any

from pyckish.event_element import EventElement


class Headers(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Headers
    """
    def __init__(self) -> None:
        super().__init__()

    def extract(self, event: dict, context: dict) -> Any:
        try:
            argument = event['headers']
        except KeyError:
            argument = {}
        return argument
