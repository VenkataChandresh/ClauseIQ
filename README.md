# ClauseIQ Backend

ClauseIQ is a multi-document legal document Q&A platform. Users will be able to upload PDF contracts or legal documents, ask questions in plain English, and receive source-backed answers from the uploaded documents.

This repository currently contains the FastAPI backend foundation for ClauseIQ.

## Current Features

- FastAPI backend setup
- Health check endpoint
- PDF upload endpoint
- PDF text extraction using PyMuPDF
- Temporary file handling so uploaded PDFs are not stored permanently

## Tech Stack

- FastAPI
- Python
- PyMuPDF
- Uvicorn
- python-dotenv

## Project Structure

```txt
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── services/
│   │   └── pdf_service.py
│   └── models/
│       └── schemas.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```txt
http://127.0.0.1:8000/docs
```

## API Endpoints

### GET `/`

Returns a basic message confirming the API is running.

### GET `/health`

Returns the backend health status.

Example response:

```json
{
  "status": "ok"
}
```

### POST `/upload`

Accepts a PDF file, extracts text from it, and returns basic metadata.

Example response:

```json
{
  "filename": "sample.pdf",
  "page_count": 3,
  "text_length": 5421,
  "message": "PDF uploaded and text extracted successfully."
}
```

## Roadmap

- Add response schemas with Pydantic
- Support multiple PDF uploads per session
- Add text chunking
- Store chunks in per-session ChromaDB collections
- Add semantic search
- Add OpenRouter LLM answers
- Add citation highlighting
- Add confidence scoring
- Add streaming responses
