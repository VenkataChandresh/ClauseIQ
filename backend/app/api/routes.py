# imports
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text_from_pdf
from app.models.schemas import RootResponse, HealthResponse, UploadResponse
from app.services.chunk_service import chunk_text

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
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:
        pdf_data = extract_text_from_pdf(temp_file_path)
        chunks = chunk_text(pdf_data["text"])

        return {
            "filename": file.filename,
            "page_count": pdf_data["page_count"],
            "text_length": pdf_data["text_length"],
            "chunk_count": len(chunks),
            "message": "PDF uploaded, text extracted, and chunked successfully.",
        }

    finally:
        os.remove(temp_file_path)
