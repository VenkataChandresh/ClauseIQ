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
    session_id: str
    document_count: int
    documents: list[DocumentUploadResult]
    message: str


class SessionDocumentSummary(BaseModel):
    filename: str
    chunk_count: int


class SessionSummaryResponse(BaseModel):
    session_id: str
    total_chunks: int
    documents: list[SessionDocumentSummary]


class AskRequest(BaseModel):
    session_id: str
    question: str


class AskResponse(BaseModel):
    session_id: str
    question: str
    answer: str
    matches: list[MatchedChunk]


class MatchedChunk(BaseModel):
    matched_filename: str
    matched_chunk_index: int
    matched_text_preview: str
    confidence_score: float
