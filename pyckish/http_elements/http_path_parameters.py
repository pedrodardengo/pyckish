from typing import Any

from pyckish.lambda_input_element import LambdaInputElement


class PathParameters(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Path Parameters
    """

    def __init__(self) -> None:
        super().__init__()

    def extract(self, event: dict, context: dict) -> Any:
        try:
            argument = event['pathParameters']
        except KeyError:
            argument = {}
        return argument
