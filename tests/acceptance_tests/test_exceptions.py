import pydantic
import pytest

import pyckish
from pyckish.exceptions.validation_error import ValidationError
from tests.examples.context_example import CONTEXT_EXAMPLE
from tests.examples.event_example import EVENT_EXAMPLE


def test_validation_error() -> None:
    # Arrange
    @pyckish.Lambda()
    def lambda_handler(
            some_value: list[int]
    ) -> list[int]:
        return some_value

    # Act and Assert
    with pytest.raises(ValidationError):
        lambda_handler(EVENT_EXAMPLE, CONTEXT_EXAMPLE)


def test_validation_error_when_validating_against_model() -> None:
    # Arrange
    class MyModel(pydantic.BaseModel):
        value: int

    @pyckish.Lambda()
    def lambda_handler(
            some_value: MyModel
    ) -> MyModel:
        return some_value

    # Act and Assert
    with pytest.raises(ValidationError):
        lambda_handler({'some_value': {'value': 'a'}}, {})


def test_validation_error_key_not_found_in_context() -> None:
    # Arrange
    @pyckish.Lambda()
    def lambda_handler(
            some_value: int
    ) -> int:
        return some_value

    # Act and Assert
    with pytest.raises(ValidationError):
        lambda_handler({}, {})
