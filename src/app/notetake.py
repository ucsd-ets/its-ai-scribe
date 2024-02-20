from . import utilities
import json
from . import config
import os

def notetake(audio_path: str, language: str, output_path: str):
    
    result = None
    if config.CACHE_TRANSCRIPT and os.path.exists(f'{output_path}/transcript.json'):    
        with open(f'{output_path}/transcript.json', 'r') as file:
            result = json.loads(file.read())
    else:
        result = utilities.transcribe(audio_path, language)
    
    # Cache transcript
    with open(f'{output_path}/transcript.json', 'w') as file:
        file.write(json.dumps(result, indent=4))
    
    segments = utilities.chunk_on_pause(result['segments'], -1, 250, 750)
    
    chapters = gen_chapters(output_path, segments)
    note_arr = gen_notes(output_path, chapters)
    sum_arr = gen_summaries(output_path, note_arr)
    abstract = gen_abstract(output_path, sum_arr)
    return gen_markdown(output_path, sum_arr, note_arr, abstract)

        
def gen_chapters(output_path, segments):
    # Create Chapter titles for segments
    # subset = segments[:5]
    subset = segments
    
    chapters = utilities.chapterize(subset)

    for c in chapters:
        print(c["title"])
        print(c["time"])
        print(c["metadata"], "\n")
        print(c["text"], "\n\n")

    gen_artifact(output_path, 'chapters', chapters)
    return chapters

def gen_notes(output_path, chapters):
    
    q = "Write structured notes ONLY in bulletpoint form using the following excerpt of a lecture transcript:\n"
    
    note_arr=[]
    for c in chapters:
        content = '\n'.join([c['title'], c['metadata'], c['text']])
        
        notes = utilities.query(q, content)
        filtered ='\n'.join([line for line in notes.split('\n') if line.strip() and line.strip()[0] in ('*', '+', '-')])
        
        print('\n', filtered, '\n')
        
        note_arr.append({'title': c['title'], 'content': filtered})
        
    gen_artifact(output_path, 'notes', note_arr)
    
    return note_arr

def gen_summaries(output_path, note_arr):
    # Make notes of the notes
    q = "Write a 1 sentence <50 characters summary of the notes provided. Please return ONLY the summary.\n"

    sum_arr = []
    for n in note_arr:
        summary = utilities.query(q, n['content'])
        print(summary)
        sum_arr.append({'title': n['title'], 'content': summary})
        
    gen_artifact(output_path, 'summary', sum_arr)
    
    return sum_arr

def gen_abstract(output_path, result):
    # Make summary of the summary
    p= "Write a 3 sentence abstract of the following notes.\n"

    with open(f'{output_path}/summary.json', 'r') as file:
        sum_arr = json.loads(file.read())

    txt = '\n'.join([s['content'] for s in sum_arr])

    abstract = utilities.query(p, txt)

    gen_artifact(output_path, 'abstract', abstract)
    
    return abstract

def gen_markdown(output_path, sum_arr, note_arr, abstract):
        # Generate the markdown file
    sections=[]

    for s, n in zip(sum_arr, note_arr):
        title = n['title']
        n_body = n['content']
        summary_body = s['content']
        
        # Format note_body into markdown
        p="Format the following notes into rich markdown.\n Indent knowledge, bold keywords, and italicize examples. Format appropriate data into tables. Last but not least, keep the headers under or equal to ###.\n"
        
        formatted = utilities.query(p, n_body)
        
        section_md = f"## {title}\n{summary_body}\n{formatted}\n"
        
        sections.append(section_md)
        print(section_md)

    md = f"""# Lecture Notes

    ## Abstract
    {abstract}

    {''.join(sections)}
    """

    with open(f'{output_path}/notes.md', 'w') as file:
        file.write(md)
        
    return md

def gen_artifact(output_path, name, result):
    with open(f'{output_path}/{name}.json', 'w') as file:
        file.write(json.dumps(result, indent=4))
        
    return f'{output_path}/{name}.json'