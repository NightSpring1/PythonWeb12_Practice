import faker
import random
from database_mogo import mongo_connect, disconnect_all
from model import Contacts


def make_fake_contacts(amount: int) -> list:
    fake = faker.Faker()
    contacts = list()
    for _ in range(amount):
        contacts.append(Contacts(fullname=fake.name(),
                                 email=fake.free_email(),
                                 phone=fake.phone_number(),
                                 is_notified=False,
                                 prioritize_email=bool(random.randint(0, 1))
                                 ))
    return contacts


if __name__ == "__main__":
    # Connections
    mongo_connect()

    # Create fake contacts
    contacts_list = make_fake_contacts(200)

    # fill database
    for contact in contacts_list:
        contact.save()

    disconnect_all()
