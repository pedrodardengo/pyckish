import inspect
import re
from abc import ABC, abstractmethod
from typing import Optional, Any

EMPTY = inspect.Parameter.empty


class LambdaInputElement(ABC):
    """
    Your custom Event Element needs to be a child of this class
    """

    def __init__(
            self,
            alias: Optional[str] = None,
            default: Any = EMPTY(),
            regex: Optional[str] = None
    ) -> None:
        self.alias = alias
        self.regex = regex
        self.default = default
        self.parameter_name: Optional[str] = None

    @abstractmethod
    def extract(self, event: dict, context: dict) -> Any:
        ...

    def select_key_for_extraction(self, keys: set[str]) -> str:
        if self.alias:
            return self.alias
        if self.regex:
            try:
                for key in keys:
                    if re.match(self.regex, key):
                        return key
            except re.error:
                raise ValueError(f'Bad regex pattern on pyckish: "{self.regex}"')
        return self.parameter_name
