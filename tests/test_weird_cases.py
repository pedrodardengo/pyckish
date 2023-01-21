import pyckish


def test_using_pyckish_on_a_parameterless_function() -> None:
    # Arrange
    @pyckish.Lambda()
    def lambda_handler() -> str:
        return 'Hello'

    # Act
    result = lambda_handler({}, {})

    # Assert
    assert result == 'Hello'
