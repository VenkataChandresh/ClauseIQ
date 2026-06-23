from pydantic import BaseModel


class RootResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


class DocumentUploadResult(BaseModel):
    filename: str
    page_count: int
    text_length: int
    chunk_count: int


class UploadResponse(BaseModel):
    document_count: int
    documents: list[DocumentUploadResult]
    message: str
