import dataclasses
import json
from typing import Any, Optional

import pyckish.types.http_codes as status


@dataclasses.dataclass
class HTTPResponse:
    body: Any = None
    headers: Optional[dict] = None
    status_code: Optional[int] = None

    def __call__(self) -> str:
        response_dict = {'isBase64Encoded': False}
        if self.body:
            response_dict['body'] = self.body
        if self.headers:
            if 'Content-Type' not in self.headers.keys():
                self.headers['Content-Type'] = 'application/json'
        else:
            self.headers = {'Content-Type': 'application/json'}
        response_dict['headers'] = self.headers
        response_dict['statusCode'] = self.status_code if self.status_code else status.HTTP_201_CREATED
        return json.dumps(response_dict)
