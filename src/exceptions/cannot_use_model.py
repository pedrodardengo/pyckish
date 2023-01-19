from src.event_elements.event_element import EventElement


class CannotUseModel(Exception):

    def __init__(self, parameter_name: str, event_element: EventElement) -> None:
        super().__init__(
            f'On parameter "{parameter_name}" cannot '
            f'extract single key from {type(event_element)}'
        )
