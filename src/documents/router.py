from fastapi import APIRouter, Depends, status, Request, Response

from .dependencies import validate_document_id
from .schemas import DocumentCreateRequest, DocumentResponse, DocumentUpdateRequest
from src.documents import service as document_service


router = APIRouter(
    prefix="/docs",
    tags=["Documents"]
)


@router.get("/")
def fetch_all_documents() -> list[DocumentResponse]:
    return document_service.get_all_documents()


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Successful Creation"}
    }
)
def add_document(document: DocumentCreateRequest, request: Request, response: Response) -> DocumentResponse:
    created_document = document_service.create_document(document)

    response.headers["Location"] = f"{request.url}{created_document.id}"

    return created_document


@router.get(
    "/{document_id}", dependencies=[Depends(validate_document_id)],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Request",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid ID: must be 24-character hex string"}
                }
            }
        }
    }
)
def fetch_single_document(document_id: str) -> DocumentResponse:
    return document_service.get_single_document(document_id)


@router.patch(
    "/{document_id}", dependencies=[Depends(validate_document_id)],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Request",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid ID: must be 24-character hex string"}
                }
            }
        }
    }
)
def update_single_document(document_id: str, update: DocumentUpdateRequest) -> DocumentResponse:
    return document_service.update_single_document(document_id, update)


@router.delete(
    "/{document_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(validate_document_id)],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful Update, No Response Provided"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Request",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid ID: must be 24-character hex string"}
                }
            }
        }
    }
)
def delete_single_document(document_id: str):
    document_service.delete_single_document(document_id)
