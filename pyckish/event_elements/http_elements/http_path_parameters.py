from typing import Any

from pyckish.event_elements.event_element import EventElement


class HTTPPathParameters(EventElement):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def extract_all(event: dict, context: dict) -> Any:
        try:
            argument = event['pathParameters']
        except KeyError:
            argument = {}
        return argument
