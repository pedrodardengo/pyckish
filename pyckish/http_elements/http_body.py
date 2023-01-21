from typing import Optional, Any

from pyckish.lambda_input_element import LambdaInputElement, LambdaInput


class Body(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts an HTTP Body
    """

    def __init__(self, default: Optional[str] = None) -> None:
        super().__init__(default=default)

    def extract(self, lambda_input: LambdaInput) -> Any:
        try:
            argument = lambda_input.event['body']
        except KeyError:
            argument = {}
        return argument
