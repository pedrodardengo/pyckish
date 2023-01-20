from pyckish import LambdaInputElement
from pyckish.exceptions.validation_error import ValidationError


class Method(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts the HTTP Method
    """

    def extract(self, event: dict, context: dict) -> str:
        try:
            return event['method']
        except KeyError:
            ValidationError('Method not present in the event')
