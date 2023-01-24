import dataclasses
import pyckish.types.http_codes as status
from typing import Any, Optional


@dataclasses.dataclass
class HTTPResponse:

    body: Any = None
    headers: Optional[dict] = None
    status_code: Optional[int] = None

    def __call__(self) -> dict:
        response_dict = {}
        if self.body:
            response_dict['Body'] = self.body
        if self.headers:
            if 'Content-Type' not in self.headers.keys():
                self.headers['Content-Type'] = 'application/json'
        else:
            self.headers = {'Content-Type': 'application/json'}
        response_dict['Headers'] = self.headers
        response_dict['StatusCode'] = self.status_code if self.status_code else status.HTTP_201_CREATED
        return response_dict
