from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, extract
from src.database.models import Contact, Phone, Email
from src.schemas import ContactIn, ContactOut


async def db_to_contact(contacts: list[Contact]) -> list[ContactOut]:
    return [
        ContactOut(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            phones=[phone.number for phone in contact.phones],
            emails=[email.address for email in contact.emails],
            birthday=contact.birthday,
            description=contact.description
        )
        for contact in contacts
    ]


async def contact_to_db(contacts: list[ContactIn]) -> list[Contact]:
    return [
        Contact(
            first_name=contact.first_name,
            last_name=contact.last_name,
            phones=[Phone(number=phone) for phone in contact.phones],
            emails=[Email(address=email) for email in contact.emails],
            birthday=contact.birthday,
            description=contact.description
        )
        for contact in contacts
    ]


async def get_contacts(skip, limit, session: AsyncSession) -> list[ContactOut]:
    async with session.begin():
        contacts = await session.execute(select(Contact).limit(limit).offset(skip))
        contacts = [contact for contact in contacts.unique().scalars()]
    return await db_to_contact(contacts)


async def get_contact(contact_id: int, session: AsyncSession) -> list[ContactOut] | None:
    async with session.begin():
        contacts = await session.execute(select(Contact).filter(Contact.id == contact_id))
    if contacts:
        contacts = [contact for contact in contacts.unique().scalars()]
        return await db_to_contact(contacts)
    else:
        return None


async def search_contacts(prompt: str, session: AsyncSession) -> list[ContactOut] | None:
    async with session.begin():
        prompt_lower = prompt.lower()
        results = await session.execute(
            select(Contact).where(
                or_(
                    func.lower(Contact.first_name).contains(prompt_lower),
                    func.lower(Contact.last_name).contains(prompt_lower),
                    Contact.emails.any(func.lower(Email.address).contains(prompt_lower)),
                    Contact.phones.any(func.lower(Phone.number).contains(prompt_lower))
                )
            )
        )
    if results:
        results = [result for result in results.unique().scalars()]
        return await db_to_contact(results)
    else:
        return None


async def add_contact(contact: ContactIn, session: AsyncSession) -> list[ContactOut]:
    async with session.begin():
        contact = await contact_to_db([contact])
        session.add_all(contact)
    return await db_to_contact(contact)


async def update_contact(contact_update: ContactIn, contact_id: int, session: AsyncSession) -> list[ContactOut] | None:
    async with session.begin():
        contact: Contact | None = await session.get(Contact, contact_id)
        if contact:
            await session.delete(*contact.phones)
            await session.delete(*contact.emails)
            contact.first_name = contact_update.first_name
            contact.last_name = contact_update.last_name
            contact.phones = [Phone(number=phone) for phone in contact_update.phones]
            contact.emails = [Email(address=email) for email in contact_update.emails]
            contact.birthday = contact_update.birthday
            contact.description = contact_update.description
            await session.commit()
            return await db_to_contact([contact])
        else:
            return None


async def search_birthdays(days, session: AsyncSession) -> list[ContactOut] | None:
    async with session.begin():
        today = date.today()
        end_date = today + timedelta(days=days)

        results = await session.execute(
            select(Contact)
            .filter(
                extract('month', Contact.birthday).between(today.month, end_date.month),
                extract('day', Contact.birthday).between(today.day, end_date.day)
            )
        )
        if results:
            results = [result for result in results.unique().scalars()]
            return await db_to_contact(results)
        else:
            return None


async def remove_contact(contact_id: int, session: AsyncSession) -> list[ContactOut] | None:
    async with session.begin():
        contact: Contact | None = await session.get(Contact, contact_id)
        if contact:
            await session.delete(contact)
            await session.flush()
            return await db_to_contact([contact])
        else:
            return None
