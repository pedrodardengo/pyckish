from abc import ABC
from typing import Optional, Any, Protocol, runtime_checkable


@runtime_checkable
class SingleValueExtraction(Protocol):

    def extract_single(self, name: str, event: dict, context: dict) -> Any:
        ...


@runtime_checkable
class AllValuesExtraction(Protocol):

    def extract_all(self, event: dict, context: dict) -> Any:
        ...


class EventElement(ABC):

    def __init__(self, alias: Optional[str] = None, default: Optional[Any] = None) -> None:
        self.alias = alias
        self.default = default
