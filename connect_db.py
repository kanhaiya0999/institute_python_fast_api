import os
from typing import Optional, Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


DATABASE_NAME: Optional[str] = os.getenv("DATABASE_NAME")
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")


client: Optional[MongoClient[Any]] = None


async def connect_db() -> Database[Any]:
    global client
    if not DATABASE_URL or not DATABASE_NAME:
        raise Exception("No database name and no database URL found")

    if client is None:
        try:
            client = MongoClient(DATABASE_URL)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    db: Database[Any] = client[DATABASE_NAME]
    return db


async def get_user_collection() -> Collection[Any]:
    db = await connect_db()

    user_collection: Collection[Any] = db["users"]
    return user_collection


async def get_class_collection() -> Collection[Any]:
    db = await connect_db()

    other_collection: Collection[Any] = db["classes"]
    return other_collection


async def get_subject_collection() -> Collection[Any]:
    db = await connect_db()

    other_collection: Collection[Any] = db["subjects"]
    return other_collection


async def get_pdf_collection() -> Collection[Any]:
    db = await connect_db()

    other_collection: Collection[Any] = db["pdfs"]
    return other_collection


async def get_video_collection() -> Collection[Any]:
    db = await connect_db()

    other_collection: Collection[Any] = db["videos"]
    return other_collection
