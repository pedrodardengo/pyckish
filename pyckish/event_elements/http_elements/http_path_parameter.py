from typing import Optional, Any

from pyckish.event_elements.event_element import EventElement
from pyckish.exceptions.validation_error import ValidationError


class HTTPPathParameter(EventElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single HTTP Path Parameter
    """
    def __init__(self, alias: Optional[str] = None) -> None:
        super().__init__(alias=alias)

    def extract(self, event: dict, context: dict) -> Any:
        key = self.alias if self.alias is not None else self.parameter_name
        try:
            argument = event['pathParameters'][key]
        except (KeyError, AttributeError):
            raise ValidationError(f'Path Parameter: "{key}" could not be found in event')
        return argument
