from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import ContactCreate, ContactRead, ContactUpdate
import crud
from typing import List

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactRead)
async def create(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(db, contact)

@router.get("/", response_model=List[ContactRead])
async def read_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(db, skip, limit)

@router.get("/{contact_id}", response_model=ContactRead)
async def read_one(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await crud.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactRead)
async def update(contact_id: int, contact: ContactUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_contact(db, contact_id, contact)

@router.delete("/{contact_id}")
async def delete(contact_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_contact(db, contact_id)

@router.get("/search/", response_model=List[ContactRead])
async def search(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(db, query)

@router.get("/birthdays/upcoming", response_model=List[ContactRead])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await crud.get_upcoming_birthdays(db)
