from faker import Faker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import randint

from src.database.models import Contact, Email, Phone, Base


postgres = ''


engine = create_engine(postgres)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

for i in range(500):
    phones = []
    emails = []
    for _ in range(randint(0, 4)):
        phones.append(Phone(number=fake.phone_number()))
    for _ in range(randint(0, 4)):
        emails.append(Email(address=fake.ascii_free_email()))

    session.add(Contact(first_name=fake.first_name(),
                        last_name=fake.last_name() if randint(0, 100) > 10 else None,
                        emails=emails,
                        phones=phones,
                        birthday=fake.date_of_birth() if randint(0, 100) > 30 else None,
                        description=fake.sentence(nb_words=10, variable_nb_words=False) if randint(0, 100) < 30 else None))
    print(i)

session.commit()
session.close()
