from pyckish import LambdaInputElement
from pyckish.exceptions.validation_error import ValidationError
from pyckish.lambda_input_element import LambdaInput


class Path(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts the HTTP Method
    """

    def extract(self, lambda_input: LambdaInput) -> str:
        try:
            return lambda_input.event['path']
        except KeyError:
            ValidationError('Path not present in the event')
