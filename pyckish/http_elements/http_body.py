import json
from typing import Any

from pyckish.lambda_input_element import LambdaInputElement


class Body(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts an HTTP Body
    """

    def __init__(self) -> None:
        super().__init__()

    def extract(self, event: dict, context: dict) -> Any:
        return json.loads(event.get('body', "{}"))
