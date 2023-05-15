from abc import ABC, abstractmethod


class Interface(ABC):
    def __init__(self):
        self.input_message: str = ''
        self.output_message: str = ''

    @abstractmethod
    def input_user_message(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def print_output_message(self) -> None:
        raise NotImplementedError


class CommandLineInterface(Interface):
    def __init__(self):
        super().__init__()

    def input_user_message(self) -> None:
        self.input_message = input('Enter Command: ')

    def print_output_message(self) -> None:
        print(self.output_message)
