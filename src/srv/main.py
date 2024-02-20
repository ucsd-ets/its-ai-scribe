from . import connectors
from fastapi import FastAPI, UploadFile, File

app = FastAPI()
app.include_router(connectors.router)