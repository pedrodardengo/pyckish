from typing import Optional, Any

from pyckish.event_element import EventElement


class Body(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts an HTTP Body
    """
    def __init__(self, default: Optional[str] = None) -> None:
        super().__init__(default=default)

    def extract(self, event: dict, context: dict) -> Any:
        try:
            argument = event['body']
        except KeyError:
            argument = {}
        return argument
