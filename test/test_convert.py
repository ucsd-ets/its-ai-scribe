import requests
import os
from src.notetake import notetake

def test_mp3_conversion():
    
    response = requests.post(
        "http://localhost:8000/convert/mp3",
        files={"file": open("test/test.mp3", "rb")}
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "File saved successfully"}

def test_yt_conversion():
    
    response = requests.post(
        "http://localhost:8000/convert/youtube",
        json={"url": "https://www.youtube.com/watch?v=gDpyBifg6-s"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "File saved successfully"}

def test_notetake():
    
    notetake("test/test.mp4", "tiny.en", "artifacts/data")
    
    assert os.path.exists("artifacts/data/transcript.json")
    assert os.path.exists("artifacts/data/chapters.json")
    assert os.path.exists("artifacts/data/notes.json")
    assert os.path.exists("artifacts/data/summaries.json")
    assert os.path.exists("artifacts/data/abstract.txt")
    assert os.path.exists("artifacts/data/notes.md")