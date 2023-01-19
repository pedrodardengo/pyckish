from pydantic import BaseModel, Field
from pydantic.fields import ModelField

from src.http_elements.path_parameters.path_parameter import PathParameter
from src.http_elements.path_parameters.path_parameters import PathParameters
from src.main import AWSEventToHTTP


class P(BaseModel):
    p_1: list[str] = Field(alias='param_1')


@AWSEventToHTTP()
def func(
        p_1: list[str] = PathParameter(alias='param_1'),
        p_2: P = PathParameters()
) -> None:
    print(p_1)
    print(p_2)


event = {
    'pathParameters': {
        'param_1': [1, 2, 3]
    },
}
context = {}

#func(event, context)

from pydantic import create_model

Strategy = create_model("Strategy", name=(str, ...), periods=(int, ...))

s = Strategy(name='pedro', periods='100')
print(s)
print(s.name)
print(Strategy.__dict__)