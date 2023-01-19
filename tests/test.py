from pydantic import BaseModel, Field

from src.event_elements.http_elements.body import Body
from src.event_elements.http_elements.header import Header
from src.event_elements.http_elements.headers import Headers
from src.event_elements.http_elements.path_parameter import PathParameter
from src.event_elements.http_elements.path_parameters import PathParameters
from src.event_elements.http_elements.query_parameter import QueryParameter
from src.main import AWSEventExtractor


class P(BaseModel):
    p_1: list[str] = Field(alias='param_1')


class H(BaseModel):
    h_1: str = '300'


class B(BaseModel):
    a: int
    b: str


@AWSEventExtractor()
def func(
        p_1: list[str] = PathParameter(alias='param_1'),
        p_2: P = PathParameters(),
        h_1: str = Header(default='200'),
        h: H = Headers(),
        b: B = Body(),
        q_4: dict = QueryParameter(alias='q_1'),
        q_5: list = QueryParameter(alias='q_3'),
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
