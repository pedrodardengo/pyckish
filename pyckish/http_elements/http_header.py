from typing import Optional, Any

from pyckish import LambdaInputElement, EMPTY
from pyckish.exceptions.validation_error import ValidationError


class Header(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single HTTP Header
    """

    def __init__(
            self,
            alias: Optional[str] = None,
            default: Any = EMPTY(),
            regex: Optional[str] = None
    ) -> None:
        super().__init__(alias=alias, default=default, regex=regex)

    def extract(self, event: dict, context: dict) -> Any:
        try:
            headers = event['headers']
            key = self.select_key_for_extraction(set(headers.keys()))
            return headers[key]
        except (KeyError, AttributeError):
            if type(self.default) == EMPTY:
                raise ValidationError(f'The header parameter "{key}" could not be found in the event')
            return self.default
