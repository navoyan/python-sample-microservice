from typing import Mapping

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from .exceptions import DocumentNotFound
from .schemas import DocumentCreateRequest, DocumentUpdateRequest, DocumentResponse

import src.database as database


def get_all_documents() -> list[DocumentResponse]:
    with database.documents_collection.find() as cursor:
        document_dicts = list(cursor)

    return list(map(lambda raw_dict: convert_to_response(raw_dict), document_dicts))


def create_document(document: DocumentCreateRequest) -> DocumentResponse:
    document_dict = jsonable_encoder(document)
    insert_result = database.documents_collection.insert_one(document_dict)

    return DocumentResponse(**document.model_dump(), id=str(insert_result.inserted_id))


def get_single_document(document_id: str) -> DocumentResponse:
    document_dict = database.documents_collection.find_one({"_id": ObjectId(document_id)})

    if document_dict is None:
        raise DocumentNotFound

    return convert_to_response(document_dict)


def update_single_document(document_id: str, update: DocumentUpdateRequest) -> DocumentResponse:
    update_result = database.documents_collection.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": update.model_dump(exclude_unset=True)}
    )

    if update_result.matched_count == 0:
        raise DocumentNotFound

    return get_single_document(document_id)


def delete_single_document(document_id: str):
    delete_result = database.documents_collection.delete_one({"_id": ObjectId(document_id)})

    if delete_result.deleted_count == 0:
        raise DocumentNotFound


def convert_to_response(document_dict: Mapping[str, any]) -> DocumentResponse:
    return DocumentResponse(**document_dict, id=str(document_dict["_id"]))
