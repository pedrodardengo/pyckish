from typing import Any


def generate_parse_error_message(
        parameter_name: str,
        raw_argument: Any,
        annotation: type
) -> str:
    return (
            f'On parameter {parameter_name} A validation error occurred when trying to parse: {type(raw_argument)} ' +
            f'to {annotation}\n value: {raw_argument}'
    )
