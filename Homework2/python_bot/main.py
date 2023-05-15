from python_bot import Bot, AddressBook


class Session:
    def __init__(self):
        self.bot = Bot()
        self.my_address_book = AddressBook()
        # self.my_address_book.fill_addressbook(20)  # Fill addressbook with fake records
        self.bot.addressbook_polling(self.my_address_book)


def main() -> None:
    Session()

if __name__ == '__main__':
    main()



