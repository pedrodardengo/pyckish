from typing import Any

from src.event_elements.event_element import EventElement


class Headers(EventElement):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def extract_all(event: dict, context: dict) -> Any:
        try:
            argument = event['headers']
        except KeyError:
            argument = {}
        return argument
