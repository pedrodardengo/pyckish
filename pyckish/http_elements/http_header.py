from typing import Optional, Any

from pyckish.event_element import EventElement, EMPTY
from pyckish.exceptions.validation_error import ValidationError


class Header(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single HTTP Header
    """
    def __init__(self, alias: Optional[str] = None, default: Any = EMPTY()) -> None:
        super().__init__(alias=alias, default=default)

    def extract(self, event: dict, context: dict) -> Any:
        key = self.alias if self.alias is not None else self.parameter_name
        try:
            return event['headers'][key]
        except (KeyError, AttributeError):
            if type(self.default) == EMPTY:
                raise ValidationError(f'The header parameter "{key}" could not be found in the event')
            return self.default
