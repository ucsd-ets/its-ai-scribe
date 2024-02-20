import os
from fastapi import APIRouter, UploadFile, File
from pytube import YouTube
from src.app.notetake import notetake
import pydantic
import ffmpeg
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/convert/mp3")
async def convert(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    
    if file.filename.endswith('.mp3'):
        with open(f'artifacts/audio/{file.filename}', 'wb') as buffer:
            buffer.write(await file.read())
        
        # Begin note taking task
        
        md = go_with_file(file.filename)
        
        return {"message": "Task finished", "notes": md}
    else:
        return {"message": "Invalid file type"}

class URL(pydantic.BaseModel):
    url: str

@router.post("/convert/youtube")
async def convert(url: URL):
    url = url.url
    
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    
    fname = stream.default_filename
    stream.download(output_path='artifacts/audio', filename=fname)
    
    # Begin note taking task
    md = go_with_file(fname)
    
    return {"message": "Task finished", "notes": md}

def go_with_file(fname):
    logger.info("Beginning note taking task")
    
    if not os.path.exists(f'artifacts/data/{fname}'):
        os.makedirs(f'artifacts/data/{fname}')
        
    md = notetake(f'artifacts/audio/{fname}', 'tiny.en', f'artifacts/data/{fname}')
    return md