from typing import Any

from pyckish.lambda_input_element import LambdaInputElement, LambdaInput


class QueryParameters(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Query String Parameters
    """

    def __init__(self) -> None:
        super().__init__()

    def extract(self, lambda_input: LambdaInput) -> Any:
        try:
            argument = lambda_input.event['queryStringParameters']
        except KeyError:
            argument = {}
        return argument
