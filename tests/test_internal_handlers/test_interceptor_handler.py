from pyckish.internal_handlers.interceptor_handler import InterceptorHandler


def test_execute_chain_of_inbound_interceptors():
    # Arrange
    event = {"test_key": "test_value"}
    context = {"test_context": "test_value"}
    interceptor_handler = InterceptorHandler([
        lambda e, c: ({"key1": "value1"}, {"key2": "value2"}),
        lambda e, c: ({"key3": "value3"}, {"key4": "value4"})
    ], None)
    expected_event = {"key3": "value3"}
    expected_context = {"key4": "value4"}

    # Act
    event, context = interceptor_handler.execute_chain_of_inbound_interceptors(event, context)

    # Assert
    assert event == expected_event
    assert context == expected_context


def test_execute_chain_of_outbound_interceptors():
    # Arrange
    output = {"test_key": "test_value"}
    interceptor_handler = InterceptorHandler(None, [
        lambda o: {"key1": "value1"},
        lambda o: {"key2": "value2"}
    ])
    expected_output = {"key2": "value2"}

    # Act
    output = interceptor_handler.execute_chain_of_outbound_interceptors(output)

    # Assert
    assert output == expected_output


def test_execute_chain_of_inbound_interceptors_with_empty_list():
    # Arrange
    event = {"test_key": "test_value"}
    context = {"test_context": "test_value"}
    interceptor_handler = InterceptorHandler([], None)

    # Act
    event, context = interceptor_handler.execute_chain_of_inbound_interceptors(event, context)

    # Assert
    assert event == {"test_key": "test_value"}
    assert context == {"test_context": "test_value"}


def test_execute_chain_of_outbound_interceptors_with_empty_list():
    # Arrange
    output = {"test_key": "test_value"}
    interceptor_handler = InterceptorHandler(None, [])

    # Act
    output = interceptor_handler.execute_chain_of_outbound_interceptors(output)

    # Assert
    assert output == {"test_key": "test_value"}


def test_execute_chain_of_inbound_interceptors_with_none():
    # Arrange
    event = {"test_key": "test_value"}
    context = {"test_context": "test_value"}
    interceptor_handler = InterceptorHandler(None, None)

    # Act
    event, context = interceptor_handler.execute_chain_of_inbound_interceptors(event, context)

    # Assert
    assert event == {"test_key": "test_value"}
    assert context == {"test_context": "test_value"}
