from pyckish import LambdaInputElement
from pyckish.lambda_input_element import LambdaInput


class Context(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    It just returns the raw context.
    """

    def extract(self, lambda_input: LambdaInput) -> dict:
        return lambda_input.context
