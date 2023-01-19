import functools
import inspect
from typing import Callable, Any, Type

import pydantic
from pydantic import BaseModel

from src.event_elements.event_element import AllValuesExtraction, SingleValueExtraction, EventElement
from src.exceptions.cannot_extract_single_key import CannotExtractSingleKey
from src.exceptions.cannot_use_model import CannotUseModel
from src.exceptions.missing_http_element import MissingHTTPElement
from src.exceptions.missing_type_hint import MissingTypeHint


class AWSEventExtractor:
    """
    AWS Event extractor and validator.
    """

    def __init__(self) -> None:
        self.event = {}
        self.context = {}
        self.__raw_parameters = {}
        self.__model_structure = {}

    def __call__(self, endpoint_function: Callable) -> Callable[[dict, dict], Any]:
        @functools.wraps(endpoint_function)
        def wrapper(event: dict, context: dict) -> Any:
            self.event = event
            self.context = context
            func_parameters = inspect.signature(endpoint_function).parameters
            for parameter in func_parameters.values():
                raw_argument, annotation = self.__extract_raw_argument_from_event(parameter)
                self.__raw_parameters[parameter.name] = raw_argument
                self.__model_structure[parameter.name] = (annotation, ...)
            FunctionParameters = pydantic.create_model("FunctionParameters", **self.__model_structure)
            model = FunctionParameters(**self.__raw_parameters)
            return endpoint_function(**(model.dict()))

        return wrapper

    def __extract_raw_argument_from_event(self, parameter: inspect.Parameter) -> tuple[Any, type]:
        annotation = self.__get_annotation(parameter)
        event_element = self.__get_http_element(parameter)
        if not self.__is_annotation_a_model(annotation):
            annotation: Type
            if not isinstance(event_element, SingleValueExtraction):
                raise CannotExtractSingleKey(parameter.name, event_element)
            raw_argument = event_element.extract_single(parameter.name, self.event, self.context)
        else:
            annotation: Type[BaseModel]
            if not isinstance(event_element, AllValuesExtraction):
                raise CannotUseModel(parameter.name, event_element)
            raw_argument = event_element.extract_all(self.event, self.context)
        return raw_argument, annotation

    @staticmethod
    def __get_annotation(parameter: inspect.Parameter) -> Type:
        if parameter.annotation == inspect.Parameter.empty:
            raise MissingTypeHint()
        return parameter.annotation

    @staticmethod
    def __get_http_element(parameter: inspect.Parameter) -> EventElement:
        if parameter.default == inspect.Parameter.empty:
            raise MissingHTTPElement()
        if not issubclass(type(parameter.default), EventElement):
            raise MissingHTTPElement()
        return parameter.default

    @staticmethod
    def __is_annotation_a_model(annotation: Type) -> bool:
        try:
            return issubclass(annotation, BaseModel)
        except TypeError:
            return False
