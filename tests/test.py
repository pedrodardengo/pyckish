from pydantic import BaseModel, Field

from pyckish import AWSEventExtractor
from pyckish.event_elements.http_elements.http_body import HTTPBody
from pyckish.event_elements.http_elements.http_header import HTTPHeader
from pyckish.event_elements.http_elements.http_headers import HTTPHeaders
from pyckish.event_elements.http_elements.http_path_parameter import HTTPPathParameter
from pyckish.event_elements.http_elements.http_path_parameters import HTTPPathParameters
from pyckish.event_elements.http_elements.http_query_parameter import HTTPQueryParameter


class P(BaseModel):
    p_1: list[str] = Field(alias='param_1')


class H(BaseModel):
    h_1: str = '300'


class B(BaseModel):
    a: int
    b: str


@AWSEventExtractor()
def func(
        p_1: list[str] = HTTPPathParameter(alias='param_1'),
        p_2: P = HTTPPathParameters(),
        h_1: str = HTTPHeader(default='200'),
        h: H = HTTPHeaders(),
        b: B = HTTPBody(),
        q_4: dict = HTTPQueryParameter(alias='q_1'),
        q_5: list = HTTPQueryParameter(alias='q_3'),
) -> None:
    print(p_1)
    print(p_2)
    print(h_1)
    print(h)
    print(b)
    print(q_4)
    print(q_5)


event = {
    'pathParameters': {
        'param_1': [1, 2, 3]
    },
    'body': {
        'a': 1,
        'b': 24242
    },
    'headers': {
    },
    'queryStringParameters': {
        'q_1': {},
        'q_3': []
    }
}
context = {}

func(event, context)
