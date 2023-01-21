import functools
import inspect
from typing import Callable, Any, Type

import pydantic
from pydantic import BaseModel

from pyckish import LambdaInputElement
from pyckish.exceptions.missing_type_hint import MissingTypeHint
from pyckish.exceptions.validation_error import ValidationError
from pyckish.lambda_input_element import LambdaInput


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
        self.__raw_parameters = {}
        self.__model_structure = {}
        self.exception_handling_dict: dict[Type[Exception], Callable] = {}

    def __call__(self, lambda_handler_function: Callable) -> Callable[[dict, dict], Any]:
        @functools.wraps(lambda_handler_function)
        def wrapper(event: dict, context: dict) -> Any:
            lambda_input = LambdaInput(event=event, context=context)
            func_parameters = inspect.signature(lambda_handler_function).parameters
            try:
                for parameter in func_parameters.values():
                    annotation = self.__get_annotation(parameter)
                    raw_argument = self.__extract_raw_argument_from_inputs(lambda_input, parameter)
                    self.__raw_parameters[parameter.name] = raw_argument
                    self.__model_structure[parameter.name] = (annotation, ...)
                model = self.__generate_model()
                return lambda_handler_function(**model.__dict__)
            except Exception as exception:
                if type(exception) in self.exception_handling_dict.keys():
                    return self.exception_handling_dict[type(exception)](lambda_input, exception)
                raise exception

        return wrapper

    def add_exception_handler(
            self,
            exception_handler: Callable[[LambdaInput, Exception], Any],
            exception: Type[Exception]
    ) -> None:
        self.exception_handling_dict = {
            exception: exception_handler
        }

    def __generate_model(self) -> pydantic.BaseModel:
        FunctionParameters = pydantic.create_model("FunctionParameters", **self.__model_structure)
        try:
            return FunctionParameters(**self.__raw_parameters)
        except pydantic.ValidationError as exc:
            raise ValidationError(str(exc.errors()))

    @staticmethod
    def __extract_raw_argument_from_inputs(
            lambda_input: LambdaInput,
            parameter: inspect.Parameter
    ) -> tuple[Any, type]:
        if not issubclass(type(parameter.default), LambdaInputElement):
            try:
                return lambda_input.event[parameter.name]
            except KeyError:
                if parameter.default == inspect.Parameter.empty:
                    raise ValidationError(f'Parameter {parameter.name} is missing')
                return parameter.default
        lambda_input_element = parameter.default
        lambda_input_element.parameter_name = parameter.name
        raw_argument = lambda_input_element.extract(lambda_input)
        return raw_argument

    @staticmethod
    def __get_annotation(parameter: inspect.Parameter) -> Type:
        if parameter.annotation == inspect.Parameter.empty:
            raise MissingTypeHint()
        return parameter.annotation

    @staticmethod
    def __is_annotation_a_model(annotation: Type) -> bool:
        try:
            return issubclass(annotation, BaseModel)
        except TypeError:
            return False
