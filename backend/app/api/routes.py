from fastapi import APIRouter

router = APIRouter()


# home route
@router.get("/")
def root():
    return {"message": "ClauseIQ API is running"}


# health route
@router.get("/health")
def health_check():
    return {"status": "ok"}
