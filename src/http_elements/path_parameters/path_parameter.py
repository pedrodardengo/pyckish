from typing import Optional, Any

from src.exceptions.validation_error import ValidationError
from src.http_elements.event_element import EventElement


class PathParameter(EventElement):
    def __init__(self, alias: Optional[str] = None) -> None:
        super().__init__(alias=alias)

    def extract_single(self, name: str, event: dict, context: dict) -> Any:
        key = self.alias if self.alias is not None else name
        try:
            argument = event['pathParameters'][key]
        except (KeyError, AttributeError):
            raise ValidationError(f'Path Parameter: "{key}" could not be found in event')
        return argument
