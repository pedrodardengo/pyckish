import functools
import inspect
from typing import Callable, Any, Type

import pydantic
from pydantic import BaseModel

from pyckish import LambdaInputElement
from pyckish.exceptions.missing_event_element import MissingEventElement
from pyckish.exceptions.missing_type_hint import MissingTypeHint


class Lambda:
    """
    AWS Event extractor and validator.

    To use it just place the decorator @pyckish.AWSEventExtractor() above your handler of your AWS Lambda function.
    Pyckish will extract, parse and validate pre-defined structures that resides in the event.

    For instance, when AWS API Gateway activates an AWS Lambda, data that were within an HTTP request will reside
    now in the Event. To quickly extract and parse that data, just like a modern back-end framework would do, use
    pyckish.

    """

    def __init__(self) -> None:
        self.event = {}
        self.context = {}
        self.__raw_parameters = {}
        self.__model_structure = {}

    def __call__(self, lambda_handler_function: Callable) -> Callable[[dict, dict], Any]:
        @functools.wraps(lambda_handler_function)
        def wrapper(event: dict, context: dict) -> Any:
            self.event = event
            self.context = context
            func_parameters = inspect.signature(lambda_handler_function).parameters
            for parameter in func_parameters.values():
                raw_argument, annotation = self.__extract_raw_argument_from_event(parameter)
                self.__raw_parameters[parameter.name] = raw_argument
                self.__model_structure[parameter.name] = (annotation, ...)
            FunctionParameters = pydantic.create_model("FunctionParameters", **self.__model_structure)
            model = FunctionParameters(**self.__raw_parameters)
            return lambda_handler_function(**model.__dict__)

        return wrapper

    def __extract_raw_argument_from_event(self, parameter: inspect.Parameter) -> tuple[Any, type]:
        annotation = self.__get_annotation(parameter)
        event_element = self.__get_event_element(parameter)
        event_element.parameter_name = parameter.name
        raw_argument = event_element.extract(self.event, self.context)
        return raw_argument, annotation

    @staticmethod
    def __get_annotation(parameter: inspect.Parameter) -> Type:
        if parameter.annotation == inspect.Parameter.empty:
            raise MissingTypeHint()
        return parameter.annotation

    @staticmethod
    def __get_event_element(parameter: inspect.Parameter) -> LambdaInputElement:
        if parameter.default == inspect.Parameter.empty:
            raise MissingEventElement()
        if not issubclass(type(parameter.default), LambdaInputElement):
            raise MissingEventElement()
        return parameter.default

    @staticmethod
    def __is_annotation_a_model(annotation: Type) -> bool:
        try:
            return issubclass(annotation, BaseModel)
        except TypeError:
            return False
