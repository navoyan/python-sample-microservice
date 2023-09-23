from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    status_code: int
    detail: any

    def __init__(self, **kwargs: dict[str, any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class InvalidDocumentId(DetailedHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid ID: must be 24-character hex string"


class DocumentNotFound(DetailedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Document with the specified ID was not found"
