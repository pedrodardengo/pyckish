from typing import Optional, Union


class ValidationError(Exception):

    def __init__(self, message: str, detail: Optional[Union[dict, list]] = None) -> None:
        super().__init__(message)
        self.__detail = detail if detail is not None else {}

    def detail(self) -> Union[dict, list]:
        return self.__detail
