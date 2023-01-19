from pydantic import BaseModel, Field

from src.http_elements.body.body import Body
from src.http_elements.headers.header import Header
from src.http_elements.headers.headers import Headers
from src.http_elements.path_parameters.path_parameter import PathParameter
from src.http_elements.path_parameters.path_parameters import PathParameters
from src.http_elements.query_parameters.query_parameter import QueryParameter
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
