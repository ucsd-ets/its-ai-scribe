import whisper
import time
import os

def transcribe(filepath, model = "base.en"):
    model = whisper.load_model(model)
    result = model.transcribe(filepath, condition_on_previous_text = True, verbose = False, no_speech_threshold= 0.5, logprob_threshold = -0.65)
    
    return result["text"]


# batch transcribe audio folder and save in whisper folder
for file in os.listdir("audio"):
    if not file.startswith('.'):
        start_time = time.time()
        print("Currently Transcribing: " + file)

        text = transcribe(os.path.join("audio", file))

        print("Completed in {:.2f} minutes.\n".format((time.time() - start_time) / 60))

        with open(os.path.join("whisper", file.split('.')[0] + ".txt"), 'w') as file:
            file.write(text)
