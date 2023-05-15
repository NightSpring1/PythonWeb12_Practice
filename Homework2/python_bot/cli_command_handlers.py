from python_bot import AddressBook
from functools import wraps


class CliCommands:
    @staticmethod
    def input_error(func):
        @wraps(func)
        def wrapper(*args):
            try:
                return func(*args)
            except IndexError as index_error:
                return index_error
            except ValueError as value_error:
                return value_error
            except KeyError as key_error:
                return key_error
            except AttributeError as attribute_error:
                return attribute_error
            except NotImplementedError:
                return "This feature is not implemented"
        return wrapper

    @staticmethod
    def welcome_message(*args) -> str:  # noqa
        message = "Hi! How can i help you?"
        return message

    @staticmethod
    def help_message(*args) -> str:  # noqa
        message = """
    Commands and their usage:
    add: 
        record 'name'                        : adds a new record with specified name.
        phone 'name' 'phone'                 : add new phone to record.
        email 'name' 'email'                 : add email to record. Can be only one.
        birthday 'name' 'birthday'           : add birthday to record. Can be only one. Birthday format dd-mm-yyyy.
    change: 
        phone 'name' 'old phone' 'new phone' : change old phone with new one.
        email 'name' 'email'                 : change email in record. 
        birthday 'name' 'birthday'           : change birthday in record. Birthday format dd-mm-yyyy.
    del: 
        record 'name'                        : delete record with specified name.
        phone 'name' 'phone'                 : delete phone from record.
        email 'name' 'email'                 : delete email from record.
        birthday 'name' 'birthday'           : delete birthday from record.
        """
        return message

    @staticmethod
    @input_error
    def add_handler(addressbook: AddressBook, *args) -> str:
        if args[0] == 'record':
            addressbook.add_record(args[1])
            message = f'New record with name {args[1]} added to addressbook.'
        elif args[0] == 'phone':
            addressbook[args[1]].add_phone(args[2])
            message = f'Phone {args[2]} added to {args[1]} record.'
        elif args[0] == 'email':
            addressbook[args[1]].set_email(args[2])
            message = f'Email {args[2]} added to {args[1]} record.'
        elif args[0] == 'birthday':
            addressbook[args[1]].set_birthday(args[2])
            message = f'Birthday {args[2]} added to {args[1]} record.'
        else:
            message = f'add does not support {args[0]} command.'
        return message

    @staticmethod
    @input_error
    def change_handler(addressbook: AddressBook, *args) -> str:
        if args[0] == 'phone':
            addressbook[args[1]].change_phone(args[2], args[3])
            message = f'Phone in record {args[1]} was changed from {args[2]} to {args[3]} record.'
        elif args[0] == 'email':
            addressbook[args[1]].set_email(args[2])
            message = f'Email in record {args[1]} was changed'
        elif args[0] == 'birthday':
            addressbook[args[1]].set_birthday(args[2])
            message = f'Birthday in record {args[1]} was changed'
        else:
            message = f'change does not support {" ".join(args)} command.'
        return message

    @staticmethod
    @input_error
    def del_handler(addressbook: AddressBook, *args) -> str:
        if args[0] == 'record':
            addressbook.del_record(args[1])
            message = f'Record with name {args[1]} was deleted from addressbook.'
        elif args[0] == 'phone':
            addressbook[args[1]].del_phone(args[2])
            message = f'Phone {args[2]} was deleted from {args[1]} record.'
        elif args[0] == 'email':
            addressbook[args[1]].del_email()
            message = f'Email was deleted from {args[1]} record.'
        elif args[0] == 'birthday':
            addressbook[args[1]].del_birthday()
            message = f'Birthday was deleted from {args[1]} record.'
        else:
            message = f'del does not support {args[0]} command.'
        return message

    @staticmethod
    def show(addressbook: AddressBook, search_query='') -> str:
        table = addressbook.show(search_query)
        return table

    @staticmethod
    def save_data(addressbook: AddressBook, *args) -> str:  # noqa
        addressbook.save_records_to_file('storage1.dat')
        return "Records have been saved."

    @staticmethod
    def load_data(addressbook: AddressBook, *args) -> str:  # noqa
        addressbook.read_records_from_file('storage1.dat')
        return "Records have been loaded."

    function = {'hello': welcome_message,
                'help': help_message,
                'add': add_handler,
                'change': change_handler,
                'del': del_handler,
                'show': show,
                'save': save_data,
                'load': load_data}
