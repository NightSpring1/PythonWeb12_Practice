from argparse import ArgumentParser, SUPPRESS


# In progress
def parser_init() -> ArgumentParser:
    parser = ArgumentParser(description="Command Parser", epilog="End.", exit_on_error=False, add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # Create the 'add' command parser
    add_parser = subparsers.add_parser("add", help="add a new record", exit_on_error=False,add_help=False)
    add_parser.add_argument('-n', "--name", help="name of the record", required=True, nargs="*")
    add_parser.add_argument('-e', "--email", help="e-mail number of the record")
    add_parser.add_argument('-p', "--phone", help="phone number of the record")
    add_parser.add_argument('-b', "--birthday", help="birthday of the record in format dd-mm-yyyy")

    # Create the 'change' command parser
    change_parser = subparsers.add_parser("change", help="Change an existing entry", exit_on_error=False, add_help=False)
    change_parser.add_argument('-n', "--name", help="Name of the entry", required=True, nargs="*")
    change_parser.add_argument('-e', "--email", help="Email number of the entry")
    change_parser.add_argument('-op', "--old-phone", help="New phone number of the entry")
    change_parser.add_argument('-np', "--new-phone", help="New phone number of the entry")
    change_parser.add_argument('-b', "--birthday", help="New birthday of the entry")

    # Create the 'del' command parser
    del_parser = subparsers.add_parser("del", help="Delete an entry", exit_on_error=False, add_help=False)
    del_parser.add_argument('-n', "--name", help="Name of the entry", required=True, nargs="*")
    del_parser.add_argument('-e', "--email", help="Email number of the entry")
    del_parser.add_argument('-p', "--phone", help="New phone number of the entry")
    del_parser.add_argument('-b', "--birthday", help="New birthday of the entry")

    # Create the 'file' command parser
    file_parser = subparsers.add_parser("file", help="Save or load from file", exit_on_error=False, add_help=False)
    file_parser.add_argument('-l', "--load", help="load from file", default=SUPPRESS, nargs='?')
    file_parser.add_argument('-s', "--save", help="save to file", default=SUPPRESS, nargs='?')

    return parser
