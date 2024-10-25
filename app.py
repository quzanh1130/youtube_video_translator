from flask import Flask, render_template, request, jsonify
from youtube_downloader import YouTubeDownloader
from audio_extractor import AudioExtractor
from transcriber import Transcriber
from translator import Translator
from subtitle_creator import SubtitleCreator
import os
import time
import torch
from utils import convert_srt_to_vtt
from config import model_name_vn_to_en, model_name_en_to_vn, device

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_link = request.form.get("youtube_link")
        direction = request.form.get("direction")

        if youtube_link:
            model_name = model_name_en_to_vn if direction == "vn_to_en" else model_name_vn_to_en
            try:
                video_url, subtitle_url = start_processing(youtube_link, model_name, direction)
                return jsonify({"video_url": video_url, "subtitle_url": subtitle_url})
          
            except ValueError as e:
                return jsonify({"error": str(e)})

    return render_template("index.html")


def start_processing(youtube_link, model_name, direction):
    timestamp = str(int(time.time()))  # Generate a unique timestamp
    video_path = f"static/video/temp_video_{timestamp}.mp4"
    audio_path = f"static/audio/temp_audio_{timestamp}.wav"
    subtitle_path = f"static/sub/temp_subtitles_{timestamp}.srt"
    subtitle_vtt_path = f"static/sub/temp_subtitles_{timestamp}.vtt"

    downloader = YouTubeDownloader(youtube_link, video_path)
    downloader.download_video()

    extractor = AudioExtractor(video_path, audio_path)
    extractor.extract_audio()

    transcriber = Transcriber(audio_path)
    segments, detected_language = transcriber.transcribe_audio()
    
    # Check if the detected language matches the selected translation direction
    if (direction == "vn_to_en" and detected_language != "vi") or (direction == "en_to_vn" and detected_language != "en"):
        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)
        raise ValueError("The detected language does not match the selected translation direction.")
    
    translator = Translator(model_name, device, direction)
    translated_segments = translator.translate_text(segments)

    subtitle_creator = SubtitleCreator(subtitle_path)
    subtitle_creator.create_subtitle_file(translated_segments)
    
    convert_srt_to_vtt(subtitle_path, subtitle_vtt_path)

    os.remove(audio_path)
    os.remove(subtitle_path)

    return video_path, subtitle_vtt_path # Return the path to the processed video and subtitle


if __name__ == "__main__":
    app.run(host='0.0.0.0')
