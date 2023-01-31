from typing import Callable, Any, Optional, Type

ExcHandler = Callable[[dict, dict, Exception], Any]


class ExceptionHandler:

    def __init__(self, exception_to_handler_mapping: Optional[dict[Type[Exception], ExcHandler]]) -> None:
        self.__exception_handling_dict = {} if exception_to_handler_mapping is None else exception_to_handler_mapping

    def deal_with_exception(
            self,
            event: dict,
            context: dict,
            exception: Exception
    ) -> Any:
        for t_exc in self.__exception_handling_dict.keys():
            if t_exc == Exception:
                continue
            if self.__exception_handling_dict.get(type(exception), None):
                result = self.__exception_handling_dict[type(exception)](event, context, exception)
                return result
            if isinstance(exception, t_exc):
                result = self.__exception_handling_dict[t_exc](event, context, exception)
                return result
        if self.__exception_handling_dict.get(Exception, None):
            result = self.__exception_handling_dict[Exception](event, context, exception)
            return result
        raise exception
