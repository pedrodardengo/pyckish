import dataclasses
import json
from typing import Any, Optional

import pydantic

import pyckish.types.http_codes as status


@dataclasses.dataclass
class HTTPResponse:
    body: Any = dataclasses.field(default_factory=lambda: {})
    headers: Optional[dict] = dataclasses.field(default_factory=lambda: {})
    status_code: Optional[int] = None

    def __call__(self, response_config: dict) -> dict:
        response_dict = {'isBase64Encoded': False}
        if self.body:
            if isinstance(self.body, pydantic.BaseModel):
                response_dict['body'] = self.body.json(**response_config)
            else:
                response_dict['body'] = json.dumps(self.body)
        if self.headers:
            if 'Content-Type' not in self.headers.keys():
                self.headers['Content-Type'] = 'application/json'
        else:
            self.headers = {'Content-Type': 'application/json'}
        response_dict['headers'] = self.headers
        response_dict['statusCode'] = self.status_code if self.status_code else status.HTTP_201_CREATED
        return response_dict
