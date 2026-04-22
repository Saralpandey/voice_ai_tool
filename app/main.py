from fastapi import FastAPI
from app.api.routes_voice import router
from fastapi.staticfiles import StaticFiles
from app.api.routes_stream import router as stream_router

app = FastAPI()
app.include_router(router)
app.include_router(stream_router)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")