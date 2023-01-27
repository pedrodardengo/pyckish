import json
from typing import Optional, Union, Any

import pydantic

from pyckish.http_elements import HTTPResponse

DictOrSetIntStr = Union[
    set[Union[int, str]],
    dict[Union[int, str], Any]
]


class ResponseHandler:

    def __init__(
            self,
            is_http: bool,
            status_code: Optional[int],
            exclude_unset: bool,
            exclude_defaults: bool,
            exclude_none: bool,
            by_alias: bool,
            include: Optional[DictOrSetIntStr],
            exclude: Optional[DictOrSetIntStr]
    ) -> None:
        self.__is_http = is_http
        self.__status_code = status_code
        self.__response_config = {
            'exclude_unset': exclude_unset,
            'exclude_defaults': exclude_defaults,
            'exclude_none': exclude_none,
            'by_alias': by_alias,
            'include': include,
            'exclude': exclude
        }

    def prepare_response(self, result: Any) -> str:
        if isinstance(result, HTTPResponse):
            result.status_code = self.__status_code if result.status_code is None else result.status_code
            return result()
        if isinstance(result, pydantic.BaseModel):
            result = json.loads(result.json(**self.__response_config))
        if self.__is_http:
            return HTTPResponse(
                body=result,
                status_code=self.__status_code
            )()
        return json.dumps(result)
