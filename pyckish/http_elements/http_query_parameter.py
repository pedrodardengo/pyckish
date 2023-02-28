from typing import Optional, Any

from pyckish.exceptions.validation_error import ValidationError
from pyckish.lambda_input_element import LambdaInputElement, EMPTY


class QueryParameter(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single HTTP Query String Parameter.
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
            query_parameters = event['queryStringParameters']
            key = self.select_key_for_extraction(set(query_parameters.keys()))
            return query_parameters[key]
        except (KeyError, AttributeError):
            if type(self.default) == EMPTY:
                raise ValidationError(f'The query string parameter "{key}" could not be found in the event')
            return self.default
