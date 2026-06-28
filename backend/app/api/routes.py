# imports
import os
import tempfile
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text_from_pdf
from app.models.schemas import (
    RootResponse,
    HealthResponse,
    UploadResponse,
    SessionSummaryResponse,
)
from app.services.chunk_service import chunk_text
from app.services.session_store import save_session_chunks, get_session_chunks
from typing import Annotated, List

router = APIRouter()


# home route
@router.get("/", response_model=RootResponse)
def root():
    return {"message": "ClauseIQ API is running"}


# health route
@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}


# upload pdf route
@router.post("/upload", response_model=UploadResponse)
async def upload_pdfs(
    files: List[UploadFile] = File(..., description="Upload up to 5 PDF files"),
):
    if len(files) > 5:
        raise HTTPException(
            status_code=400,
            detail="You can upload a maximum of 5 PDF files.",
        )
    session_id = str(uuid.uuid4())
    documents = []
    all_chunks = []
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a PDF file.",
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        try:
            pdf_data = extract_text_from_pdf(temp_file_path)
            chunks = chunk_text(pdf_data["text"])
            for index, chunk in enumerate(chunks):
                all_chunks.append(
                    {
                        "session_id": session_id,
                        "filename": file.filename,
                        "chunk_index": index,
                        "text": chunk,
                    }
                )

            documents.append(
                {
                    "filename": file.filename,
                    "page_count": pdf_data["page_count"],
                    "text_length": pdf_data["text_length"],
                    "chunk_count": len(chunks),
                }
            )

        finally:
            os.remove(temp_file_path)

    save_session_chunks(session_id, all_chunks)
    return {
        "session_id": session_id,
        "document_count": len(documents),
        "documents": documents,
        "message": "PDFs uploaded, text extracted, and chunked successfully.",
    }


@router.get("/sessions/{session_id}", response_model=SessionSummaryResponse)
def get_session_summary(session_id: str):
    chunks = get_session_chunks(session_id)

    if chunks is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    document_counts = {}

    for chunk in chunks:
        filename = chunk["filename"]
        document_counts[filename] = document_counts.get(filename, 0) + 1

    documents = [
        {
            "filename": filename,
            "chunk_count": chunk_count,
        }
        for filename, chunk_count in document_counts.items()
    ]

    return {
        "session_id": session_id,
        "total_chunks": len(chunks),
        "documents": documents,
    }
