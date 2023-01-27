from typing import Any

import pyckish
from pyckish.exceptions.validation_error import ValidationError
from pyckish.http_elements import Method
from tests.examples.event_example import EVENT_EXAMPLE


def test_error_handling_for_validation_error() -> None:
    # Arrange
    error_message = {'message': 'validation error'}

    def handle_validation_error(event: dict, context: dict, exception: Exception) -> Any:
        return error_message

    @pyckish.Lambda(
        exception_to_handler_mapping={ValidationError: handle_validation_error}
    )
    def lambda_handler(method: str = Method()) -> str:
        return method

    # Act
    result = lambda_handler({}, {})

    # Assert
    assert result == error_message


def test_error_handling_for_some_error() -> None:
    # Arrange
    error_message = {'message': 'An error'}

    def handle_validation_error(event: dict, context: dict, exception: Exception) -> dict:
        return error_message

    @pyckish.Lambda(
        exception_to_handler_mapping={KeyError: handle_validation_error}
    )
    def lambda_handler(method: str = Method()) -> str:
        if method:
            raise KeyError()
        return method

    # Act
    result = lambda_handler(EVENT_EXAMPLE, {})

    # Assert
    assert result == error_message


def test_error_handling_generic_error() -> None:
    # Arrange
    error_message = {'message': 'An error'}

    def handle_validation_error(event: dict, context: dict, exception: Exception) -> dict:
        return error_message

    @pyckish.Lambda(
        exception_to_handler_mapping={Exception: handle_validation_error}
    )
    def lambda_handler(method: str = Method()) -> str:
        if method:
            raise KeyError
        return method

    # Act
    result = lambda_handler(EVENT_EXAMPLE, {})

    # Assert
    assert result == error_message
