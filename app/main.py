from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from app.api.api import api_router

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        content={
            "meta": {"code": exc.status_code, "message": str(exc.detail)},
            "data": None,
        },
        status_code=exc.status_code,
    )


app.include_router(api_router)
