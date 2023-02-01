import functools
from typing import Callable, Any, Type, Optional

from pyckish.internal_handlers.exception_handler import ExceptionHandler, ExcHandler
from pyckish.internal_handlers.interceptor_handler import InterceptorHandler, InboundInterceptor, OutboundInterceptor
from pyckish.internal_handlers.parameter_handler import ParameterHandler
from pyckish.internal_handlers.response_handler import ResponseHandler, DictOrSetIntStr


class Lambda:
    """
    To use it just place the decorator @pyckish.Lambda() above your handler of your AWS Lambda function.
    Pyckish will extract, parse and validate pre-defined structures that resides in the event.

    For instance, when AWS API Gateway activates an AWS Lambda, data that were within an HTTP request will reside
    now in the Event. To quickly extract and parse that data, just like a modern back-end framework would do, use
    pyckish.

    """

    def __init__(
            self,
            is_http: bool = False,
            response_status_code: Optional[int] = None,
            response_headers: Optional[dict[str, Any]] = None,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            response_model_by_alias: bool = False,
            response_model_include: Optional[DictOrSetIntStr] = None,
            response_model_exclude: Optional[DictOrSetIntStr] = None,
            exception_to_handler_mapping: Optional[dict[Type[Exception], ExcHandler]] = None,
            inbound_interceptors: Optional[list[InboundInterceptor]] = None,
            outbound_interceptors: Optional[list[OutboundInterceptor]] = None
    ) -> None:
        self.__interceptor_handler = InterceptorHandler(inbound_interceptors, outbound_interceptors)
        self.__parameter_handler = ParameterHandler()
        self.__exception_handler = ExceptionHandler(exception_to_handler_mapping)
        self.__response_handler = ResponseHandler(
            is_http=is_http,
            headers=response_headers,
            status_code=response_status_code,
            exclude_unset=response_model_exclude_unset,
            exclude_defaults=response_model_exclude_defaults,
            exclude_none=response_model_exclude_none,
            by_alias=response_model_by_alias,
            include=response_model_include,
            exclude=response_model_exclude
        )

    def __call__(self, lambda_handler_function: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(lambda_handler_function)
        def wrapper(event: dict, context: dict) -> Any:
            try:
                intercepted_event, intercepted_context = \
                    self.__interceptor_handler.execute_chain_of_inbound_interceptors(event, context)

                parameter_value_dict = self.__parameter_handler.generate_parameter_value_dict_for_lambda_function(
                    intercepted_event, intercepted_context, lambda_handler_function
                )
                result = lambda_handler_function(**parameter_value_dict)
                result = self.__interceptor_handler.execute_chain_of_outbound_interceptors(result)
            except Exception as exception:
                result = self.__exception_handler.deal_with_exception(event, context, exception)
            return self.__response_handler.prepare_response(result)

        return wrapper
