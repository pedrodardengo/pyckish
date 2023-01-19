from typing import Optional, Any

from src.event_elements.event_element import EventElement


class QueryParameter(EventElement):
    def __init__(self, alias: Optional[str] = None, default: Optional[Any] = None) -> None:
        super().__init__(alias=alias, default=default)

    def extract_single(self, name: str, event: dict, context: dict) -> Any:
        key = self.alias if self.alias is not None else name
        try:
            argument = event['queryStringParameters'][key]
        except (KeyError, AttributeError):
            argument = self.default
        return argument
