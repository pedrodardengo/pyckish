from typing import Any

from pyckish import LambdaInputElement
from pyckish.lambda_input_element import LambdaInput


class Headers(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts all HTTP Headers
    """

    def __init__(self) -> None:
        super().__init__()

    def extract(self, lambda_input: LambdaInput) -> Any:
        try:
            argument = lambda_input.event['headers']
        except KeyError:
            argument = {}
        return argument
