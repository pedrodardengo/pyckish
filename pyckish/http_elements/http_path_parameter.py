from typing import Optional, Any

from pyckish import LambdaInputElement
from pyckish.exceptions.validation_error import ValidationError


class PathParameter(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single HTTP Path Parameter
    """

    def __init__(self, alias: Optional[str] = None, regex: Optional[str] = None) -> None:
        super().__init__(alias=alias, regex=regex)

    def extract(self, event: dict, context: dict) -> Any:
        try:
            path_parameters = event['pathParameters']
            key = self.select_key_for_extraction(set(path_parameters.keys()))
            argument = path_parameters[key]
        except (KeyError, AttributeError):
            raise ValidationError(f'Path Parameter: "{key}" could not be found in event')
        return argument
