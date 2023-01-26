from pyckish import LambdaInputElement


class Context(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    It just returns the raw context.
    """

    def extract(self, event: dict, context: dict) -> dict:
        return context
