# imports
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import extract_text_from_pdf

router = APIRouter()


# home route
@router.get("/")
def root():
    return {"message": "ClauseIQ API is running"}


# health route
@router.get("/health")
def health_check():
    return {"status": "ok"}


# upload pdf route
@router.post("/upload")
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

        return {
            "filename": file.filename,
            "page_count": pdf_data["page_count"],
            "text_length": pdf_data["text_length"],
            "message": "PDF uploaded and text extracted successfully.",
        }

    finally:
        os.remove(temp_file_path)
