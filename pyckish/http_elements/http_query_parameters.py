from typing import Any

from pyckish.event_element import EventElement


class QueryParameters(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Query String Parameters
    """
    def __init__(self) -> None:
        super().__init__()

    def extract(self, event: dict, context: dict) -> Any:
        try:
            argument = event['queryStringParameters']
        except KeyError:
            argument = {}
        return argument
