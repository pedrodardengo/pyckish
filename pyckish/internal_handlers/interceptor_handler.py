from typing import Callable, Any, Optional

InboundInterceptor = Callable[[dict, dict], tuple[dict, dict]]
OutboundInterceptor = Callable[[Any], Any]


class InterceptorHandler:

    def __init__(
            self,
            inbound_interceptors: Optional[list[InboundInterceptor]],
            outbound_interceptors: Optional[list[OutboundInterceptor]]
    ) -> None:
        self.__inbound_interceptors = [] if inbound_interceptors is None else inbound_interceptors
        self.__outbound_interceptors = [] if outbound_interceptors is None else outbound_interceptors

    def execute_chain_of_inbound_interceptors(self, event: dict, context: dict) -> tuple[dict, dict]:
        for interceptor in self.__inbound_interceptors:
            event, context = interceptor(event, context)
        return event, context

    def execute_chain_of_outbound_interceptors(self, output: Any) -> tuple[dict, dict]:
        for interceptor in self.__outbound_interceptors:
            output = interceptor(output)
        return output
