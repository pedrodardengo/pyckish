import pytest

from pyckish.internal_handlers.exception_handler import ExceptionHandler


def test_deal_with_exception_with_matching_handler():
    # Arrange
    exception_to_handler_mapping = {ValueError: lambda e, c, exc: 'value error handled'}
    exception_handler = ExceptionHandler(exception_to_handler_mapping)
    event, context = {'event_data': 'data'}, {}
    exception = ValueError('test error')

    # Act
    result = exception_handler.deal_with_exception(event, context, exception)

    # Assert
    assert result == 'value error handled'


def test_deal_with_exception_with_no_matching_handler():
    # Arrange
    exception_to_handler_mapping = {ValueError: lambda e, c, exc: 'value error handled'}
    exception_handler = ExceptionHandler(exception_to_handler_mapping)
    event, context = {'event_data': 'data'}, {}
    exception = KeyError('test error')

    # Act and Assert
    with pytest.raises(KeyError):
        exception_handler.deal_with_exception(event, context, exception)


def test_deal_with_exception_with_default_handler():
    # Arrange
    exception_to_handler_mapping = {Exception: lambda e, c, exc: 'default exception handled'}
    exception_handler = ExceptionHandler(exception_to_handler_mapping)
    event, context = {'event_data': 'data'}, {}
    exception = KeyError('test error')

    # Act
    result = exception_handler.deal_with_exception(event, context, exception)

    # Assert
    assert result == 'default exception handled'


def test_deal_with_exception_exception_instance():
    # Arrange
    exception_to_handler_mapping = {
        ValueError: lambda e, c, exc: "ValueError handled",
        Exception: lambda e, c, exc: "Default Exception handled"
    }
    exc_handler = ExceptionHandler(exception_to_handler_mapping)
    event, context = {}, {}
    exception = Exception("Test Exception")

    # Act
    result = exc_handler.deal_with_exception(event, context, exception)

    # Assert
    assert result == "Default Exception handled"


def test_deal_with_exception_parent_handler():
    # Arrange
    exception_to_handler_mapping = {
        Exception: lambda e, c, exc: "Default Exception handled",
        ValueError: lambda e, c, exc: "ValueError handled"
    }
    exc_handler = ExceptionHandler(exception_to_handler_mapping)
    event, context = {}, {}

    class CustomException(ValueError):
        pass

    custom_exception = CustomException("Test Custom Exception")

    # Act
    result = exc_handler.deal_with_exception(event, context, custom_exception)
    # Assert
    assert result == "ValueError handled"
