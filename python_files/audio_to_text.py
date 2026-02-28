import whisper

model = whisper.load_model("base")


def audio_text(file):
    result = model.transcribe(file)
    transcript = result["text"]
    return transcript
