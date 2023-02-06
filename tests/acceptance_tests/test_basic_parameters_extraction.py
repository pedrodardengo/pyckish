import pyckish
from pyckish.basic_elements import Event, Context, EventElement, ContextElement
from tests.examples.context_example import CONTEXT_EXAMPLE
from tests.examples.event_example import EVENT_EXAMPLE


def test_extraction_for_basic_parameters() -> None:
    @pyckish.Lambda()
    def lambda_handler(
            some_value: int,
            value: str = EventElement(alias='some_value'),
            c_value: float = ContextElement(regex='value_1'),
            event: dict = Event(),
            context: dict = Context()
    ) -> None:
        assert some_value == 200
        assert value == '200'
        assert c_value == 1.4
        assert event == EVENT_EXAMPLE
        assert context == CONTEXT_EXAMPLE

    lambda_handler(EVENT_EXAMPLE, CONTEXT_EXAMPLE)
