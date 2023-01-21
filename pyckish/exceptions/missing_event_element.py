class MissingEventElement(Exception):

    def __init__(self) -> None:
        super().__init__(
            'AWSEventToHTTP: It is required to use a LambdaInputElement child class as a default value on all '
            'parameters in order to specify which parameter corresponds to which data present in the event/context'
        )
