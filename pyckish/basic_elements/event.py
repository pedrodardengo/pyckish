from pyckish import LambdaInputElement


class Event(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    It just returns the raw event.
    """

    def extract(self, event: dict, context: dict) -> dict:
        return event
