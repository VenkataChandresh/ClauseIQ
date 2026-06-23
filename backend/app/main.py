# imports
from fastapi import FastAPI
from app.api.routes import router
from fastapi.openapi.utils import get_openapi

# initializing the app
app = FastAPI(
    title="ClauseIQ API",
    description="Backend API for ClauseIQ, a legal document Q&A platform.",
    version="0.1.0",
)

# takes all the routes from the router and includes in the app
app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    body = schema["components"]["schemas"].get("Body_upload_pdfs_upload_post", {})
    files_prop = body.get("properties", {}).get("files", {})
    if "items" in files_prop:
        files_prop["items"] = {"type": "string", "format": "binary"}

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
