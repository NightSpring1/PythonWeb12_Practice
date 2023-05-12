import re
import pickle
from abc import ABC, abstractmethod
from datetime import date
from collections import UserDict
from faker import Faker
from random import randint
from prettytable.colortable import ColorTable, Themes


class _Field(ABC):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError

    @value.setter
    @abstractmethod
    def value(self, value):
        raise NotImplementedError


class _Name(_Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value) -> None:
        name_value_pattern = ''  # r'^[A-Za-zА-Яа-я .їЇєЄ]{2,35}$'
        if re.match(name_value_pattern, value):
            self._value = value
        else:
            raise ValueError("Name is not valid. It should contain only letters and be no longer than 35 characters.")


class _Phone(_Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        if not re.compile(r'^\+(?:\d[\s-]?){9,20}\d$|\d{9,15}$').match(value):
            raise ValueError("Phone number is not valid!")
        self._value = value

    def __eq__(self, _obj) -> bool:
        return self.value == _obj.value


class _Email(_Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        if not re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').match(value):
            raise ValueError("Provided email is not valid")
        self._value = value

    def __str__(self) -> str:
        return self._value


class _Birthday(_Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self) -> date:
        return self._value

    @value.setter
    def value(self, value) -> None:
        email_value_pattern = r"[-|_|\\|/]"
        day, month, year = map(int, re.split(email_value_pattern, value))
        birthday = date(year, month, day)
        if birthday >= date.today():
            raise ValueError(f"Birthday must be in the past")
        self._value = birthday

    def __str__(self) -> str:
        return self._value.strftime("%d-%m-%Y")


class _Record:
    def __init__(self, name: str):
        self.name = _Name(name)
        self.phones = []
        self.birthday = None
        self.email = None

    def add_phone(self, phone: str):
        phone = _Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)
        else:
            raise ValueError(f"Phone {phone.value} already exists in {self.name.value} record")

    def change_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        else:
            raise KeyError(f"Phone {old_phone} is not found in record")

    def del_phone(self, phone: str):
        phone = _Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise KeyError(f"Phone {phone.value} does not exist in {self.name.value} record")

    def set_birthday(self, birthday: str):
        birthday = _Birthday(birthday)
        self.birthday = birthday

    def del_birthday(self):
        self.birthday = None

    def set_email(self, email: str):
        email = _Email(email)
        self.email = email

    def del_email(self):
        self.email = None

    def days_to_birthday(self) -> int | None:
        if not self.birthday:
            return None
        today = date.today()
        try:
            birthday_this_year = self.birthday.value.replace(year=today.year)
        except ValueError:
            birthday_this_year = self.birthday.value.replace(year=today.year, day=today.day - 1)
        if birthday_this_year < today:
            birthday_this_year = self.birthday.value.replace(year=today.year + 1)
        days_to_birthday = (birthday_this_year - today).days
        return days_to_birthday

    def __str__(self):
        str_phones = ' '.join(phone.value for phone in self.phones)
        str_email = self.email.value if self.email else str()
        str_birthday = str(self.birthday) if self.birthday else str()
        return '|'.join((self.name.value, str_email, str_phones, str_birthday))


class AddressBook(UserDict):
    def add_record(self, name: str):
        if name not in self.data:
            self.data[name] = _Record(name)
        else:
            raise KeyError("Record with this name already exists.")

    def del_record(self, name: str):
        if name in self.data:
            self.data.pop(name)
        else:
            raise KeyError(f"Record with name {name} does not exist")

    def get_all_records(self) -> list[_Record]:
        records = []
        for record in self.data.values():
            records.append(record)
        return records

    def get_searched_records(self, search_query: str) -> list[_Record]:
        records = []
        for record in self.data.values():
            if search_query in str(record):
                records.append(record)
        return records

    def show(self, search_query='') -> str:
        table = ColorTable(theme=Themes.OCEAN)
        table.field_names = ["Name", "E-mail", "Phone(s)", "Birthday"]
        for record in self.data.values():
            if search_query in str(record):
                name = record.name.value
                email = record.email.value if record.email else "-"
                birthday = str(record.birthday) if record.birthday else "-"
                phones = ", ".join([phone.value for phone in record.phones]) if record.phones else "-"
                table.add_row([name, email, phones, birthday])
        return str(table)

    def save_records_to_file(self, filename: str):
        with open(filename, "wb") as fw:
            pickle.dump(self.data, fw)

    def read_records_from_file(self, filename: str):
        try:
            with open(filename, "rb") as fr:
                content = pickle.load(fr)
                self.data.update(content)
        except FileNotFoundError:
            pass

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(f"Contact with name {key} not found.")

    def fill_addressbook(self, num_of_records: int) -> None:
        fake = Faker()
        i = 0
        while i < num_of_records:
            name = fake.first_name()
            try:
                self.add_record(name)
            except KeyError:
                continue
            for _ in range(randint(0, 3)):
                self[name].add_phone(fake.msisdn())
            for _ in range(randint(0, 1)):
                self[name].set_birthday(fake.date_of_birth().strftime("%d-%m-%Y"))
            for _ in range(randint(0, 1)):
                self[name].set_email(fake.ascii_email())
            i += 1


if __name__ == '__main__':
    addressbook = AddressBook()
    addressbook.read_records_from_file('storage1.dat')
    addressbook.add_record("Alexander")
    addressbook["Alexander"].add_phone('111111111')
    addressbook["Alexander"].add_phone('111111112')
    addressbook["Alexander"].add_phone('111111113')
    addressbook["Alexander"].set_birthday('30-09-2022')
    addressbook["Alexander"].set_email('abcdef@gmail.com')
    addressbook["Alexander"].del_phone('111111112')
    print(addressbook.show())
