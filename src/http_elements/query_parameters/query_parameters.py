from typing import Any

from src.http_elements.http_element import HTTPElement


class QueryParameters(HTTPElement):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def extract_all(event: dict, context: dict) -> Any:
        try:
            argument = event['queryStringParameters']
        except KeyError:
            argument = {}
        return argument
