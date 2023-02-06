import datetime

import pydantic

import pyckish
from pyckish.http_elements import Body, Header, Headers, PathParameter, PathParameters, \
    QueryParameter, QueryParameters, Method, Path
from tests.examples.event_example import EVENT_EXAMPLE
from tests.examples.http_models import UserPathParameters, UserHeaders, UserQueryParameters, UserBody


def test_extraction_for_path_parameters() -> None:
    @pyckish.Lambda()
    def lambda_handler(
            param_1: int = PathParameter(),
            param_2: str = PathParameter(alias='p_2'),
            p_params: UserPathParameters = PathParameters()
    ) -> None:
        assert param_1 == 200
        assert param_2 == 'someRandomCharacters'
        assert isinstance(p_params, pydantic.BaseModel)
        assert p_params.dict() == {'param_1': 200, 'param_2': 'someRandomCharacters'}

    lambda_handler(EVENT_EXAMPLE, {})


def test_extraction_for_headers() -> None:
    @pyckish.Lambda()
    def lambda_handler(
            header_1: list[int] = Header(),
            header_2: set[str] = Header(),
            header_3: int = Header(default=300),
            headers: UserHeaders = Headers(),
    ) -> None:
        assert header_1 == [1, 2, 3]
        assert header_2 == {'1', '2', '3'}
        assert header_3 == 300
        assert isinstance(headers, pydantic.BaseModel)
        assert headers.dict() == {'header_1': [1, 2, 3], 'header_2': {'1', '2', '3'}}

    lambda_handler(EVENT_EXAMPLE, {})


def test_extraction_for_query_parameters() -> None:
    @pyckish.Lambda()
    def lambda_handler(
            query_1: datetime.date = QueryParameter(alias='q_1'),
            query_2: list[dict] = QueryParameter(alias='q_2', regex='q_3'),
            query_3: dict = QueryParameter(regex='q_3', default={}),
            q_params: UserQueryParameters = QueryParameters()
    ) -> None:
        assert isinstance(query_1, datetime.date)
        assert query_1.isoformat() == '1996-12-01'
        assert query_2 == []
        assert query_3 == {}
        assert isinstance(q_params, pydantic.BaseModel)

    lambda_handler(EVENT_EXAMPLE, {})


def test_extraction_for_body() -> None:
    @pyckish.Lambda()
    def lambda_handler(
            body: UserBody = Body()
    ) -> None:
        assert isinstance(body, pydantic.BaseModel)
        assert isinstance(body.body_1, pydantic.BaseModel)

    lambda_handler(EVENT_EXAMPLE, {})


def test_extraction_for_other_http_elements() -> None:
    @pyckish.Lambda()
    def lambda_handler(
            path: str = Path(),
            method: str = Method()
    ) -> None:
        assert path == '/a/big/path'
        assert method == 'GET'

    lambda_handler(EVENT_EXAMPLE, {})
