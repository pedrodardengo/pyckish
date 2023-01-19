from typing import Optional, Any

from src.http_elements.http_element import HTTPElement


class Body(HTTPElement):
    def __init__(self, default: Optional[str] = None) -> None:
        super().__init__(default=default)

    @staticmethod
    def extract_all(event: dict, context: dict) -> Any:
        try:
            argument = event['body']
        except KeyError:
            argument = {}
        return argument
