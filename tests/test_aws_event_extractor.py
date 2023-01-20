import datetime

import pyckish
import pydantic

from pyckish.http_elements import Body
from pyckish.http_elements import Header
from pyckish.http_elements import Headers
from pyckish.http_elements import PathParameter
from pyckish.http_elements import PathParameters
from pyckish.http_elements import QueryParameter
from pyckish.http_elements import QueryParameters
from tests.examples.event_example import EVENT_EXAMPLE
from tests.examples.http_models import UserPathParameters, UserHeaders, UserQueryParameters, UserBody


def test_aws_event_extract() -> None:
    @pyckish.AWSEventExtractor()
    def lambda_handler(
            # Path Parameters
            param_1: int = PathParameter(),
            param_2: str = PathParameter(alias='p_2'),
            p_params: UserPathParameters = PathParameters(),

            # Headers
            header_1: list[int] = Header(),
            header_2: set[str] = Header(),
            header_3: int = Header(default=300),
            headers: UserHeaders = Headers(),

            # Query Parameters
            query_1: datetime.date = QueryParameter(alias='q_1'),
            query_2: list[dict] = QueryParameter(alias='q_2'),
            query_3: dict = QueryParameter(alias='q_3', default={}),
            q_params: UserQueryParameters = QueryParameters(),

            # Body
            body: UserBody = Body()
    ) -> None:
        # Path Parameters
        assert param_1 == 200
        assert param_2 == 'someRandomCharacters'
        assert isinstance(p_params, pydantic.BaseModel)
        assert p_params.dict() == {'param_1': 200, 'param_2': 'someRandomCharacters'}

        # Headers
        assert header_1 == [1, 2, 3]
        assert header_2 == {'1', '2', '3'}
        assert header_3 == 300
        assert isinstance(headers, pydantic.BaseModel)
        assert headers.dict() == {'header_1': [1, 2, 3], 'header_2': {'1', '2', '3'}}

        # Query Parameters
        assert isinstance(query_1, datetime.date)
        assert query_1.isoformat() == '1996-12-01'
        assert query_2 == []
        assert query_3 == {}
        assert isinstance(q_params, pydantic.BaseModel)

        # Body
        assert isinstance(body, pydantic.BaseModel)
        assert isinstance(body.body_1, pydantic.BaseModel)

    lambda_handler(EVENT_EXAMPLE, {})
