import pyckish
import pytest

from pyckish.exceptions.missing_type_hint import MissingTypeHint
from pyckish.exceptions.validation_error import ValidationError
from tests.examples.context_example import CONTEXT_EXAMPLE
from tests.examples.event_example import EVENT_EXAMPLE


def test_extraction_for_basic_parameters() -> None:
    # Arrange
    @pyckish.Lambda()
    def lambda_handler(
            some_value
    ) -> int:
        return some_value

    # Act and Assert
    with pytest.raises(MissingTypeHint):
        lambda_handler(EVENT_EXAMPLE, CONTEXT_EXAMPLE)


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
