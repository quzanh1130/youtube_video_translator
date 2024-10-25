import time

class SubtitleCreator:
    def __init__(self, subtitle_path):
        self.subtitle_path = subtitle_path

    def create_subtitle_file(self, translated_segments):
        with open(self.subtitle_path, 'w') as f:
            for i, (start, end, text) in enumerate(translated_segments):
                start_time_formatted = time.strftime('%H:%M:%S', time.gmtime(start)) + ',' + str(int((start % 1) * 1000)).zfill(3)
                end_time_formatted = time.strftime('%H:%M:%S', time.gmtime(end)) + ',' + str(int((end % 1) * 1000)).zfill(3)
                f.write(f"{i+1}\n")
                f.write(f"{start_time_formatted} --> {end_time_formatted}\n")
                f.write(f"{text}\n\n")

