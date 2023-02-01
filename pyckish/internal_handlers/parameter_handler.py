import inspect
from typing import Callable, Any, Type

import pydantic

from pyckish import LambdaInputElement
from pyckish.exceptions.validation_error import ValidationError


class ParameterHandler:

    def __init__(self) -> None:
        self.__raw_parameters = {}
        self.__model_structure = {}

    def generate_parameter_value_dict_for_lambda_function(
            self,
            event: dict,
            context: dict,
            lambda_handler_function: Callable[..., Any]
    ) -> dict:
        func_parameters = inspect.signature(lambda_handler_function).parameters
        for parameter in func_parameters.values():
            annotation = self.__get_annotation(parameter)
            raw_argument = self.__extract_raw_argument_from_inputs(
                event, context, parameter
            )
            self.__raw_parameters[parameter.name] = raw_argument
            self.__model_structure[parameter.name] = (annotation, ...)
        model = self.__generate_model()
        return model.__dict__

    def __generate_model(self) -> pydantic.BaseModel:
        FunctionParameters = pydantic.create_model("FunctionParameters", **self.__model_structure)
        try:
            return FunctionParameters(**self.__raw_parameters)
        except pydantic.ValidationError as exc:
            raise ValidationError('Validation Error', detail=exc.errors())

    @staticmethod
    def __get_annotation(parameter: inspect.Parameter) -> Type:
        if parameter.annotation == inspect.Parameter.empty:
            return Any
        return parameter.annotation

    @staticmethod
    def __extract_raw_argument_from_inputs(
            event: dict,
            context: dict,
            parameter: inspect.Parameter
    ) -> Any:
        if not issubclass(type(parameter.default), LambdaInputElement):
            raw_argument = event.get(parameter.name, parameter.default)
            if parameter.default == inspect.Parameter.empty and raw_argument is None:
                raise ValidationError(f'Parameter {parameter.name} is missing')
            return raw_argument
        lambda_input_element = parameter.default
        lambda_input_element.parameter_name = parameter.name
        raw_argument = lambda_input_element.extract(event, context)
        return raw_argument
