from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status, Path

from src.database.db import get_session
from src.schemas import ContactIn, ContactOut
from src.repository import contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/all", response_model=list[ContactOut])
async def read_contacts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    """Retrieve all contacts.

    Parameters:
    - skip (int): Number of contacts to skip (default: 0).
    - limit (int): Maximum number of contacts to retrieve (default: 100).

    Returns:
    - list[ContactOut]: List of ContactOut objects representing the retrieved contacts.

    Raises:
    - HTTPException: If no contacts are found, returns HTTP 404 Not Found.
    """
    all_contacts = await contacts.get_contacts(skip, limit, db)
    if all_contacts:
        return all_contacts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")


@router.get("/{contact_id}", response_model=list[ContactOut])
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_session)):
    """Retrieve a specific contact by ID.

        Parameters:
        - contact_id (int): ID of the contact to retrieve.

        Returns:
        - list[ContactOut]: List containing a single ContactOut object representing the retrieved contact.

        Raises:
        - HTTPException: If the contact with the specified ID is not found, returns HTTP 404 Not Found.
        """
    all_contacts = await contacts.get_contact(contact_id, db)
    if all_contacts:
        return all_contacts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")


@router.get("/search/{prompt}", response_model=list[ContactOut])
async def search_contact(prompt: str, db: AsyncSession = Depends(get_session)):
    """Search for contacts matching the given prompt.

        Parameters:
        - prompt (str): Search prompt to find matching contacts.

        Returns:
        - list[ContactOut]: List of ContactOut objects representing the matching contacts.

        Raises:
        - HTTPException: If no contacts matching the prompt are found, returns HTTP 404 Not Found.
        """
    all_contacts = await contacts.search_contacts(prompt, db)
    if all_contacts:
        return all_contacts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")


@router.get("/birthdays/{days}", response_model=list[ContactOut])
async def get_birthdays(days: int = Path(..., ge=1, le=7), db: AsyncSession = Depends(get_session)):
    """Retrieve contacts with birthdays within the specified number of days.

        Parameters:
        - days (int): Number of days to consider for upcoming birthdays.

        Returns:
        - list[ContactOut]: List of ContactOut objects representing the contacts with upcoming birthdays.

        Raises:
        - HTTPException: If no contacts with upcoming birthdays are found, returns HTTP 404 Not Found.
        """
    all_contacts = await contacts.search_birthdays(days, db)
    if all_contacts:
        return all_contacts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")


@router.post("/create", response_model=list[ContactOut], status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactIn, db: AsyncSession = Depends(get_session)):
    """Create a new contact.

        Parameters:
        - contact (ContactIn): ContactIn object representing the contact to be created.

        Returns:
        - list[ContactOut]: List containing a single ContactOut object representing the created contact.

        Raises:
        - HTTPException: If the contact cannot be created, returns the appropriate HTTP status code and detail message.
        """
    contact = await contacts.add_contact(contact, db)
    return contact


@router.put("/update/{contact_id}", response_model=list[ContactOut])
async def update_contact(contact: ContactIn, contact_id: int, db: AsyncSession = Depends(get_session)):
    """Update an existing contact.

        Parameters:
        - contact (ContactIn): ContactIn object representing the updated contact information.
        - contact_id (int): ID of the contact to update.

        Returns:
        - list[ContactOut]: List containing a single ContactOut object representing the updated contact.

        Raises:
        - HTTPException: If the contact with the specified ID is not found, returns HTTP 404 Not Found.
        """
    contact = await contacts.update_contact(contact, contact_id, db)
    if contact:
        return contact
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")


@router.delete("/delete/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_session)):
    """Delete a contact.

        Parameters:
        - contact_id (int): ID of the contact to delete.

        Raises:
        - HTTPException: If the contact with the specified ID is not found, returns HTTP 404 Not Found.
        """
    contact = await contacts.remove_contact(contact_id, db)
    if contact:
        return contact
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
