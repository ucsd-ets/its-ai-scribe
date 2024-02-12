import sys
import json
sys.path.append("..")
from src.utilities import *

result = transcribe("../artifacts/audio/example.mp3", "medium.en")

# Segment the transcript on all pauses
segments = chunk_on_pause(result['segments'], -1, 250, 1500)

with open('tmp.txt', 'w') as f:
    f.write(json.dumps(segments))