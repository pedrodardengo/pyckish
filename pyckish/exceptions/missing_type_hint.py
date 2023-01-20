class MissingTypeHint(Exception):

    def __init__(self) -> None:
        super().__init__('AWSEventToHTTP: It is required to use type hints on all of the inputs')
