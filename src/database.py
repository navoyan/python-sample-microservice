from contextlib import asynccontextmanager

from pymongo import MongoClient
from pymongo.collection import Collection

from .config import settings


documents_collection: Collection


@asynccontextmanager
async def lifespan(_):
    global documents_collection

    mongo_client = MongoClient(settings.mongo_url)
    database = mongo_client.get_database(settings.database_name)

    collection_name = settings.collection_name
    if collection_name in database.list_collection_names():
        documents_collection = database.get_collection(collection_name)
    else:
        documents_collection = database.create_collections(collection_name)

    yield

    mongo_client.close()
    documents_collection = None
