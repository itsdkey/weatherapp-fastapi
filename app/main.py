from fastapi import FastAPI

from opeanweather.routers import opeanweather_router

app = FastAPI()
app.include_router(opeanweather_router, prefix="/weather", tags=["weather"])


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}
