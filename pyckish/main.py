import functools
import inspect
from typing import Callable, Any, Type, Optional, Union

import pydantic

from pyckish import LambdaInputElement
from pyckish.exceptions.validation_error import ValidationError
from pyckish.http_elements.http_response import HTTPResponse


class Lambda:
    """
    AWS Event extractor and validator.

    To use it just place the decorator @pyckish.AWSEventExtractor() above your handler of your AWS Lambda function.
    Pyckish will extract, parse and validate pre-defined structures that resides in the event.

    For instance, when AWS API Gateway activates an AWS Lambda, data that were within an HTTP request will reside
    now in the Event. To quickly extract and parse that data, just like a modern back-end framework would do, use
    pyckish.

    """

    def __init__(
            self,
            is_http: bool = False,
            response_status_code: Optional[int] = None,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            response_model_by_alias: bool = False,
            response_model_include: Optional[Union[set[Union[int, str]], dict[Union[int, str], Any]]] = None,
            response_model_exclude: Optional[Union[set[Union[int, str]], dict[Union[int, str], Any]]] = None,
            exception_to_handler_mapping: Optional[
                dict[Type[Exception], Callable[[dict, dict, Exception], Any]]
            ] = None,
            inbound_interceptors: Optional[list[Callable[[dict, dict], tuple[dict, dict]]]] = None,
            outbound_interceptors: Optional[list[Callable[[Any], Any]]] = None
    ) -> None:
        self.__is_http = is_http
        self.__response_status_code = response_status_code
        self.__response_config = {
            'exclude_unset': response_model_exclude_unset,
            'exclude_defaults': response_model_exclude_defaults,
            'exclude_none': response_model_exclude_none,
            'by_alias': response_model_by_alias,
            'include': response_model_include,
            'exclude': response_model_exclude
        }
        self.__raw_parameters = {}
        self.__model_structure = {}
        self.__inbound_interceptors = [] if inbound_interceptors is None else inbound_interceptors
        self.__outbound_interceptors = [] if outbound_interceptors is None else outbound_interceptors
        self.__exception_handling_dict = {} if exception_to_handler_mapping is None else exception_to_handler_mapping

    def __call__(self, lambda_handler_function: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(lambda_handler_function)
        def wrapper(event: dict, context: dict) -> Any:
            func_parameters = inspect.signature(lambda_handler_function).parameters
            try:
                intercepted_event, intercepted_context = self.__execute_chain_of_inbound_interceptors(event, context)
                for parameter in func_parameters.values():
                    annotation = self.__get_annotation(parameter)
                    raw_argument = self.__extract_raw_argument_from_inputs(
                        intercepted_event, intercepted_context, parameter
                    )
                    self.__raw_parameters[parameter.name] = raw_argument
                    self.__model_structure[parameter.name] = (annotation, ...)
                model = self.__generate_model()
                result = lambda_handler_function(**model.__dict__)
                result = self.__execute_chain_of_outbound_interceptors(result)
            except Exception as exception:
                if type(exception) in self.__exception_handling_dict.keys():
                    return self.__exception_handling_dict[type(exception)](event, context, exception)
                raise exception
            return self.__prepare_response(result)

        return wrapper

    def add_exception_handler(
            self,
            exception_handler: Callable[[dict, dict, Exception], Any],
            exception: Type[Exception]
    ) -> None:
        self.__exception_handling_dict = {
            exception: exception_handler
        }

    def __execute_chain_of_inbound_interceptors(self, event: dict, context: dict) -> tuple[dict, dict]:
        for interceptor in self.__inbound_interceptors:
            event, context = interceptor(event, context)
        return event, context

    def __execute_chain_of_outbound_interceptors(self, output: Any) -> tuple[dict, dict]:
        for interceptor in self.__outbound_interceptors:
            output = interceptor(output)
        return output

    def __prepare_response(self, result: Any) -> Any:
        if isinstance(result, HTTPResponse):
            result.status_code = self.__response_status_code if result.status_code is None else result.status_code
            return result()
        if isinstance(result, pydantic.BaseModel):
            result = result.dict(**self.__response_config)
        if self.__is_http:
            return HTTPResponse(
                body=result,
                status_code=self.__response_status_code
            )()
        return result

    def __generate_model(self) -> pydantic.BaseModel:
        FunctionParameters = pydantic.create_model("FunctionParameters", **self.__model_structure)
        try:
            return FunctionParameters(**self.__raw_parameters)
        except pydantic.ValidationError as exc:
            raise ValidationError(str(exc.errors()))

    @staticmethod
    def __extract_raw_argument_from_inputs(
            event: dict,
            context: dict,
            parameter: inspect.Parameter
    ) -> tuple[Any, type]:
        if not issubclass(type(parameter.default), LambdaInputElement):
            try:
                return event[parameter.name]
            except KeyError:
                if parameter.default == inspect.Parameter.empty:
                    raise ValidationError(f'Parameter {parameter.name} is missing')
                return parameter.default
        lambda_input_element = parameter.default
        lambda_input_element.parameter_name = parameter.name
        raw_argument = lambda_input_element.extract(event, context)
        return raw_argument

    @staticmethod
    def __get_annotation(parameter: inspect.Parameter) -> Type:
        if parameter.annotation == inspect.Parameter.empty:
            return Any
        return parameter.annotation

    @staticmethod
    def __is_annotation_a_model(annotation: Type) -> bool:
        try:
            return issubclass(annotation, pydantic.BaseModel)
        except TypeError:
            return False
