import requests
import os
from src.app.notetake import notetake

response = requests.post(
    "http://localhost:8000/convert/mp3",
    files={"file": open("test/test.mp3", "rb")}
)

print(response.status_code)
print(response.json()) 