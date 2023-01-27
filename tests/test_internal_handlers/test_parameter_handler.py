import pydantic
import pytest

from pyckish.basic_elements import EventElement, ContextElement
from pyckish.exceptions.validation_error import ValidationError
from pyckish.internal_handlers.parameter_handler import ParameterHandler


def test_parameter_handler() -> None:
    # Arrange
    class AModel(pydantic.BaseModel):
        a: int

    event = {'v_1': 1, 'v_2': '2', 'v_3': {'a': '3'}, 'value_6': ['1', '2']}
    context = {'value_8': '8'}
    parameter_handler = ParameterHandler()

    def lambda_handler(
            v_1,
            v_2: int,
            v_3: AModel,
            v_4=4,
            v_5: int = 5,
            v_6: list[int] = EventElement(alias='value_6'),
            v_7: int = EventElement(alias='value_7', default=7),
            v_8: int = ContextElement(alias='value_8', default=1)
    ):
        ...

    # Act
    parameter_value_dict = parameter_handler.generate_parameter_value_dict_for_lambda_function(
        event, context, lambda_handler
    )

    # Assert
    assert parameter_value_dict == {
        'v_1': 1, 'v_2': 2, 'v_3': AModel(a=3), 'v_4': 4, 'v_5': 5, 'v_6': [1, 2], 'v_7': 7, 'v_8': 8
    }


def test_parameter_handler_validation_error() -> None:
    # Arrange
    parameter_handler = ParameterHandler()

    def lambda_handler(
            some_value: list[int]
    ) -> list[int]:
        return some_value

    # Act and Assert
    with pytest.raises(ValidationError):
        parameter_handler.generate_parameter_value_dict_for_lambda_function(
            {}, {}, lambda_handler
        )
