import inspect
from abc import ABC, abstractmethod
from typing import Optional, Any


EMPTY = inspect.Parameter.empty


class EventElement(ABC):
    """
    Your custom Event Element needs to be a child of this class
    """

    def __init__(self, alias: Optional[str] = None, default: Any = EMPTY()) -> None:
        self.alias = alias
        self.default = default
        self.parameter_name: Optional[str] = None

    @abstractmethod
    def extract(self, event: dict, context: dict) -> Any:
        ...
