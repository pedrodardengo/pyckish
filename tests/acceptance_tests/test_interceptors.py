import pyckish
from pyckish.basic_elements import Event


def test_inbound_interceptors() -> None:
    # Arrange
    pyckish_lambda = pyckish.Lambda(
        inbound_interceptors=[
            lambda e, c: ({**e, 1: 1}, c),
            lambda e, c: ({**e, 2: 2}, c),
            lambda e, c: ({**e, 3: 3}, c),
        ]
    )

    @pyckish_lambda
    def lambda_handler(event: dict = Event()) -> dict:
        return event

    # Act
    result = lambda_handler({}, {})

    # Assert
    assert result == {1: 1, 2: 2, 3: 3}


def test_outbound_interceptors() -> None:
    # Arrange
    pyckish_lambda = pyckish.Lambda(
        outbound_interceptors=[
            lambda r: r + 1,
            lambda r: r + 2,
            lambda r: r + 3,
        ]
    )

    @pyckish_lambda
    def lambda_handler(value: int) -> int:
        return value

    # Act
    result = lambda_handler({'value': 1}, {})

    # Assert
    assert result == 7
