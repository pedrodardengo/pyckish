import functools
import inspect
import json
from typing import Callable, Any, Type

import typeguard
from pydantic import BaseModel

from src.exceptions.cannot_extract_single_key import CannotExtractSingleKey
from src.exceptions.cannot_use_model import CannotUseModel
from src.exceptions.missing_http_element import MissingHTTPElement
from src.exceptions.missing_type_hint import MissingTypeHint
from src.exceptions.parsing_error import generate_parse_error_message
from src.exceptions.validation_error import ValidationError
from src.http_elements.http_element import HTTPElement, AllValuesExtraction, SingleValueExtraction


class AWSEventToHTTP:

    def __call__(self, endpoint_function: Callable) -> Callable[[dict, dict], Any]:
        @functools.wraps(endpoint_function)
        def wrapper(event: dict, context: dict) -> Any:
            func_parameters = inspect.signature(endpoint_function).parameters
            passed_parameters = {}

            for parameter in func_parameters.values():
                annotation = self.__get_annotation(parameter)
                http_element = self.__get_http_element(parameter)
                if not self.__is_annotation_a_model(annotation):
                    annotation: Type
                    if not isinstance(http_element, SingleValueExtraction):
                        raise CannotExtractSingleKey(parameter.name, http_element)
                    raw_argument = http_element.extract_single(parameter.name, event, context)
                    validated_argument = self.__validate_to_primitive(parameter.name, raw_argument, annotation)
                else:
                    annotation: Type[BaseModel]
                    if not isinstance(http_element, AllValuesExtraction):
                        raise CannotUseModel(parameter.name, http_element)
                    raw_argument = http_element.extract_all(event, context)
                    validated_argument = self.__validate_to_model(parameter.name, raw_argument, annotation)

                passed_parameters[parameter.name] = validated_argument

            return endpoint_function(**passed_parameters)

        return wrapper

    @staticmethod
    def __get_annotation(parameter: inspect.Parameter) -> Type:
        if parameter.annotation == inspect.Parameter.empty:
            raise MissingTypeHint()
        return parameter.annotation

    @staticmethod
    def __get_http_element(parameter: inspect.Parameter) -> HTTPElement:
        if parameter.default == inspect.Parameter.empty:
            raise MissingHTTPElement()
        if not issubclass(type(parameter.default), HTTPElement):
            raise MissingHTTPElement()
        return parameter.default

    @staticmethod
    def __is_annotation_a_model(annotation: Type) -> bool:
        try:
            return issubclass(annotation, BaseModel)
        except TypeError:
            return False

    @staticmethod
    def __validate_to_primitive(name: str, raw_argument: Any, annotation: Type) -> Any:
        if typeguard.check_type(name, raw_argument, annotation):
            return raw_argument
        try:
            return annotation(raw_argument)
        except Exception:
            raise ValidationError(generate_parse_error_message(name, raw_argument, annotation))

    @staticmethod
    def __validate_to_model(name: str, raw_argument: Any, annotation: Type[BaseModel]) -> BaseModel:
        if isinstance(raw_argument, str):
            try:
                raw_argument = json.loads(raw_argument)
            except json.decoder.JSONDecodeError:
                raise ValidationError(generate_parse_error_message(name, raw_argument, annotation))
        elif not isinstance(raw_argument, dict):
            raise ValidationError(generate_parse_error_message(name, raw_argument, annotation))
        return annotation(**raw_argument)
