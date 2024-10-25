import yt_dlp as youtube_dl

class YouTubeDownloader:
    def __init__(self, youtube_link, output_path):
        self.youtube_link = youtube_link
        self.output_path = output_path

    def download_video(self):
        ydl_opts = {
            'format': 'best',
            'outtmpl': self.output_path,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtube_link])
