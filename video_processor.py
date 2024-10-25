import subprocess

class VideoProcessor:
    def __init__(self, video_path, subtitle_path, output_path):
        self.video_path = video_path
        self.subtitle_path = subtitle_path
        self.output_path = output_path

    def add_subtitles(self):
        subprocess.run(["ffmpeg", "-i", self.video_path, "-vf", f"subtitles={self.subtitle_path}", self.output_path], check=True)

    def play_video(self):
        subprocess.run(["ffplay", self.output_path])
