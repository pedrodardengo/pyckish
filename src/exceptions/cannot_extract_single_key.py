from src.http_elements.event_element import EventElement


class CannotExtractSingleKey(Exception):

    def __init__(self, parameter_name: str, event_element: EventElement) -> None:
        super().__init__(
                f'On parameter "{parameter_name}" cannot '
                f'extract {type(event_element)} as a Model'
        )
