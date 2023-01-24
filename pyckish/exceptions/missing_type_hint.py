class MissingTypeHint(Exception):
    MESSAGE = 'Pyckish: It is required to use type hints on all of the inputs'

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)
