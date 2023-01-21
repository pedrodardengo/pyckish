from pyckish import LambdaInputElement
from pyckish.lambda_input_element import LambdaInput


class Event(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    It just returns the raw event.
    """

    def extract(self, lambda_input: LambdaInput) -> dict:
        return lambda_input.event
