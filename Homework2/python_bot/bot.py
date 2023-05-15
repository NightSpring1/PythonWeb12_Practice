from python_bot import CliCommands, CommandLineInterface, AddressBook


class Bot:
    def __init__(self):
        self.interface = CommandLineInterface()
        self.commands = CliCommands()
        self.is_working = False

    @staticmethod
    def command_parser(input_string: str) -> tuple[str, list[str]]:
        if not input_string:
            return '', ['']
        input_string = input_string.strip().lstrip()
        command = input_string.split()[0].lower()
        arguments = input_string.split()[1:]
        return command, arguments

    def addressbook_polling(self, addressbook: AddressBook):
        self.is_working = True
        while self.is_working:
            self.interface.input_user_message()
            instructions = self.command_parser(self.interface.input_message)
            if instructions[0] in self.commands.function:
                self.interface.output_message = self.commands.function[instructions[0]](addressbook, *instructions[1])
            elif instructions[0] in ('exit', 'close', 'bye'):
                self.interface.output_message = "Good bye!"
                self.is_working = False
            else:
                self.interface.output_message = "Command is not supported!"
            self.interface.print_output_message()
