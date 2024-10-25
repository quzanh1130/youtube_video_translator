import whisper

class Transcriber:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.model = whisper.load_model("base")

    def transcribe_audio(self):
        # Load audio and transcribe
        result = self.model.transcribe(self.audio_path)
        segments = result["segments"]

        # Ensure there are segments and extract the text from the first segment
        if not segments:
            raise ValueError("No segments found in the audio transcription.")

        language = result["language"]
        print(f"Detected language: {language}")

        return segments, language
