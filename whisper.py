import whisper #https://pypi.org/project/openai-whisper/

def transcribe(filepath, model = "base.en"):
    """
    Transcribes speech from an audio file using a Whisper ASR model.

    Parameters:
    - filepath (str): The path to the audio file. (supports most audio/video formats)
    - model (str): The name or path of the Whisper ASR model to use. Defaults to "base.en".
        ^ see https://github.com/openai/whisper#available-models-and-languages for more options

    Returns:
    - str: The transcribed text from the audio.

    """
    
    model = whisper.load_model(model)
    result = model.transcribe(filepath, condition_on_previous_text = True, verbose = False, no_speech_threshold= 0.5, logprob_threshold = -0.65)
    
    return result["text"]

