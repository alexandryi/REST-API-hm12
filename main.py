from fastapi import FastAPI
from routers import contacts
from database import engine, Base

app = FastAPI(title="Контактна книга API")

app.include_router(contacts.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "API працює!"}

