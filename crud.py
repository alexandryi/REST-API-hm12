from sqlalchemy.future import select
from sqlalchemy import or_, extract
from models import Contact
from schemas import ContactCreate, ContactUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

async def create_contact(db: AsyncSession, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()

async def get_contact(db: AsyncSession, contact_id: int):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalar_one_or_none()

async def update_contact(db: AsyncSession, contact_id: int, contact_data: ContactUpdate):
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        for key, value in contact_data.dict().items():
            setattr(db_contact, key, value)
        await db.commit()
        await db.refresh(db_contact)
    return db_contact

async def delete_contact(db: AsyncSession, contact_id: int):
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
    return db_contact

async def search_contacts(db: AsyncSession, query: str):
    result = await db.execute(
        select(Contact).where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
    )
    return result.scalars().all()

async def get_upcoming_birthdays(db: AsyncSession):
    today = date.today()
    next_week = today + timedelta(days=7)

    result = await db.execute(select(Contact))
    contacts = result.scalars().all()

    upcoming = []
    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = contact.birthday.replace(year=today.year + 1)

        if today <= birthday_this_year <= next_week:
            upcoming.append(contact)

    return upcoming

