from typing import Any

from pyckish.lambda_input_element import LambdaInputElement, LambdaInput


class PathParameters(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Path Parameters
    """

    def __init__(self) -> None:
        super().__init__()

    def extract(self, lambda_input: LambdaInput) -> Any:
        try:
            argument = lambda_input.event['pathParameters']
        except KeyError:
            argument = {}
        return argument
