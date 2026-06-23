# imports
from fastapi import FastAPI
from app.api.routes import router

# initializing the app
app = FastAPI(
    title="ClauseIQ API",
    description="Backend API for ClauseIQ, a legal document Q&A platform.",
    version="0.1.0",
)

# takes all the routes from the router and includes in the app
app.include_router(router)
