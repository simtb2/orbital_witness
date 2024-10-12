from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.v1.routes import router as v1_router

app = FastAPI()
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Orbital Witness"}

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "This Page Does Not Exist!"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."}
    )
