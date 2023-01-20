from pyckish import LambdaInputElement
from pyckish.exceptions.validation_error import ValidationError


class Path(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts the HTTP Method
    """

    def extract(self, event: dict, context: dict) -> str:
        try:
            return event['path']
        except KeyError:
            ValidationError('Path not present in the event')
