import datetime

import pydantic

"""These are just models used for testing purposes"""


class UserHeader(pydantic.BaseModel):
    header_1: list[int]
    header_2: set[str]


class AModel(pydantic.BaseModel):
    value_1: float = pydantic.Field(alias='body_1_1')
    value_2: datetime.date = pydantic.Field(alias='body_1_1')


class UserBody(pydantic.BaseModel):
    body_1: AModel
    body_2: set[int]


class UserPathParameter(pydantic.BaseModel):
    param_1: int
    param_2: str


class UserQueryParam(pydantic.BaseModel):
    q_1: datetime.date
    q_3: list
