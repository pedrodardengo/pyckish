from typing import Optional, Any

from pyckish.event_elements.event_element import EventElement, EMPTY
from pyckish.exceptions.validation_error import ValidationError


class HTTPQueryParameter(EventElement):
    def __init__(self, alias: Optional[str] = None, default: Any = EMPTY()) -> None:
        super().__init__(alias=alias, default=default)

    def extract_single(self, name: str, event: dict, context: dict) -> Any:
        key = self.alias if self.alias is not None else name
        try:
            return event['queryStringParameters'][key]
        except (KeyError, AttributeError):
            if type(self.default) == EMPTY:
                raise ValidationError(f'The query string parameter "{key}" could not be found in the event')
            return self.default
