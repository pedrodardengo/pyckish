import pyckish
import pydantic
from pyckish import HTTPPathParameter, HTTPPathParameters, HTTPHeader, \
    HTTPHeaders, HTTPQueryParameter, HTTPQueryParameters, HTTPBody
from tests.examples.event_example import EVENT_EXAMPLE
from tests.examples.http_models import UserPathParameter, UserHeader, UserQueryParam, UserBody


def test_aws_event_extract() -> None:

    @pyckish.AWSEventExtractor()
    def lambda_handler(
            param_1: int = HTTPPathParameter(),
            param_2: str = HTTPPathParameter(),
            p_params: UserPathParameter = HTTPPathParameters()
    ) -> None:
        assert param_1 == 200
        assert param_2 == 'someRandomCharacters'
        assert isinstance(p_params, pydantic.BaseModel)
        assert p_params.dict() == {'param_1': 200, 'param_2': 'someRandomCharacters'}

    lambda_handler(EVENT_EXAMPLE, {})
