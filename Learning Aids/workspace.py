import sys
sys.path.append("..")
from utilities import *

result = transcribe("../audio/example.mp3", "medium.en")


# Segment the transcript on all pauses
segments = chunk_on_pause(result['segments'], -1, 250, 1500)

# Create Chapter titles for segments
chapters = chapterize(segments[:5])

for c in chapters:
    print(c["title"])
    print(c["time"])
    print(c["metadata"], "\n")
    print(c["text"], "\n\n")


# q = "Imagine you are attending the lecture and tasked with refining the following excerpt into notes. Your goal is to streamline the content by eliminating redundancies and extraneous details. As you organize the notes, feel free to create subheadings where necessary. Your focus should be on retaining crucial information.\n\n"
q = "Write structured notes ONLY in bulletpoint form using the following excerpt of a lecture transcript:\n"

for c in chapters:
    content = '\n'.join([c['title'], c['metadata'], c['text']])
    
    notes = query(q, content)
    filtered ='\n'.join([line for line in notes.split('\n') if line.strip() and line.strip()[0] in ('*', '+', '-')])
    
    print('\n', filtered, '\n')