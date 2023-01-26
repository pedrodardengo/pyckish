import typing

from pyckish import LambdaInputElement, EMPTY
from pyckish.exceptions.validation_error import ValidationError


class ContextElement(LambdaInputElement):
    """
    Use this class on your Lambda Handler Function.
    Extracts a single key from the aws Context
    """

    def __init__(self, alias: typing.Optional[str] = None, default: typing.Any = EMPTY()) -> None:
        super().__init__(alias=alias, default=default)

    def extract(self, event: dict, context: dict) -> typing.Any:
        key = self.alias if self.alias is not None else self.parameter_name
        try:
            return context[key]
        except (KeyError, AttributeError):
            if type(self.default) == EMPTY:
                raise ValidationError(f'The context parameter "{key}" could not be found')
            return self.default
