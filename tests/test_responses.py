import json
from typing import Optional

import pydantic

import pyckish
import pyckish.types.http_codes as status
from pyckish.http_elements.http_response import HTTPResponse
from tests.examples.event_example import EVENT_EXAMPLE


def test_http_response_non_dict_return() -> None:
    # Arrange
    message = 'Hello World'

    @pyckish.Lambda(
        is_http=True,
        response_status_code=status.HTTP_201_CREATED
    )
    def lambda_handler() -> str:
        return message

    # Act
    response = lambda_handler(EVENT_EXAMPLE, {})

    # Assert
    assert json.loads(response) == {
        'isBase64Encoded': False,
        'body': message,
        'headers': {'Content-Type': 'application/json'},
        'statusCode': status.HTTP_201_CREATED
    }


def test_http_response_model_return() -> None:
    # Arrange
    class Item(pydantic.BaseModel):
        value_1: int = pydantic.Field(alias='Value')
        value_2: str
        value_3: int = 300
        value_4: Optional[int]

        class Config:
            allow_population_by_field_name = True

    @pyckish.Lambda(
        is_http=True,
        response_status_code=status.HTTP_202_ACCEPTED,
        response_model_by_alias=True,
        response_model_exclude={'value_2'},
        response_model_exclude_defaults=True
    )
    def lambda_handler() -> Item:
        return Item(value_1=300, value_2='a')

    # Act
    response = lambda_handler(EVENT_EXAMPLE, {})

    # Assert
    assert json.loads(response) == {
        'isBase64Encoded': False,
        'body': {
            'Value': 300
        },
        'headers': {'Content-Type': 'application/json'},
        'statusCode': status.HTTP_202_ACCEPTED
    }


def test_http_response_as_response() -> None:
    # Arrange
    @pyckish.Lambda(
        is_http=True,
        response_status_code=status.HTTP_201_CREATED
    )
    def lambda_handler() -> HTTPResponse:
        return HTTPResponse(
            body='Hello World',
            headers={'my_header': 'a_value'},
            status_code=status.HTTP_201_CREATED
        )

    # Act
    response = lambda_handler(EVENT_EXAMPLE, {})

    # Assert
    assert json.loads(response) == {
        'isBase64Encoded': False,
        'body': 'Hello World',
        'headers': {
            'Content-Type': 'application/json',
            'my_header': 'a_value'
        },
        'statusCode': status.HTTP_201_CREATED
    }
