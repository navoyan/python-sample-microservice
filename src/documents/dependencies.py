from bson import ObjectId

from .exceptions import InvalidDocumentId


def validate_document_id(document_id: str):
    if not ObjectId.is_valid(document_id):
        raise InvalidDocumentId
