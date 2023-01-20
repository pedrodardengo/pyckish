from typing import Any

from pyckish.event_element import EventElement


class PathParameters(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Path Parameters
    """
    def __init__(self) -> None:
        super().__init__()

    def extract(self, event: dict, context: dict) -> Any:
        try:
            argument = event['pathParameters']
        except KeyError:
            argument = {}
        return argument
