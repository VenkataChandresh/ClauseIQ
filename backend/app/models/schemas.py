from pydantic import BaseModel


class RootResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


class UploadResponse(BaseModel):
    filename: str
    page_count: int
    text_length: int
    chunk_count: int
    message: str
