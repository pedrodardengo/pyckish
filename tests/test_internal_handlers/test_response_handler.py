import json

import pydantic

from pyckish.http_elements import HTTPResponse
from pyckish.internal_handlers.response_handler import ResponseHandler


class AModel(pydantic.BaseModel):
    id: int
    name: str
    description: str = 'test'


def test_prepare_response_with_http_response():
    # Arrange
    http_response = HTTPResponse(body={'test': 'body'}, status_code=200)
    response_handler = ResponseHandler(
        is_http=True,
        headers=None,
        status_code=None,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        by_alias=False,
        include=None,
        exclude=None
    )

    # Act
    result = response_handler.prepare_response(http_response)

    # Assert
    result['body'] = json.loads(result['body'])
    assert result == {
        "isBase64Encoded": False,
        "body": {"test": "body"},
        "headers": {'Content-Type': 'application/json'},
        "statusCode": 200
    }


def test_prepare_response_with_pydantic_model():
    # Arrange
    model = AModel(id=1, name='test')
    response_handler = ResponseHandler(
        is_http=True,
        headers={'my_header': 200},
        status_code=None,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        by_alias=False,
        include=None,
        exclude=None
    )

    # Act
    result = response_handler.prepare_response(model)

    # Assert
    result['body'] = json.loads(result['body'])
    assert result == {
        "isBase64Encoded": False,
        "body": {"id": 1, "name": "test", "description": "test"},
        "headers": {'Content-Type': 'application/json', 'my_header': 200},
        "statusCode": 201
    }


def test_prepare_response_with_dict_input():
    # Arrange
    response_handler = ResponseHandler(
        is_http=True,
        headers={},
        status_code=None,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        by_alias=False,
        include=None,
        exclude=None
    )

    # Act
    result = response_handler.prepare_response({'test': 'body'})

    # Assert
    result['body'] = json.loads(result['body'])
    assert result == {
        "isBase64Encoded": False,
        "body": {"test": "body"},
        "headers": {'Content-Type': 'application/json'},
        "statusCode": 201
    }
