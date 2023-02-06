from typing import Optional, Any

from pyckish import LambdaInputElement, EMPTY
from pyckish.exceptions.validation_error import ValidationError


class EventElement(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single key from the AWS Event
    """

    def __init__(
            self,
            alias: Optional[str] = None,
            default: Any = EMPTY(),
            regex: Optional[str] = None
    ) -> None:
        super().__init__(alias=alias, default=default, regex=regex)

    def extract(self, event: dict, context: dict) -> Any:
        key = self.select_key_for_extraction(set(event.keys()))
        try:
            return event[key]
        except (KeyError, AttributeError):
            if type(self.default) == EMPTY:
                raise ValidationError(f'The event parameter "{key}" could not be found')
            return self.default
