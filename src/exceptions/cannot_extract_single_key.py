from src.http_elements.http_element import HTTPElement


class CannotExtractSingleKey(Exception):

    def __init__(self, parameter_name: str, http_element: HTTPElement) -> None:
        super().__init__(
                f'On parameter "{parameter_name}" cannot '
                f'extract {type(http_element)} as a Model'
        )
