import os
from moviepy.editor import VideoFileClip

class AudioExtractor:
    @staticmethod
    def extract_audio(video_file):
        mp3_file = video_file.replace('.mp4', '.mp3')
        if not os.path.exists(mp3_file):
            video_clip = VideoFileClip(video_file)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(mp3_file)
            audio_clip.close()
            video_clip.close()
            print(f"Áudio MP3 extraído e salvo em: {mp3_file}")
        else:
            print(f"Áudio MP3 já existe: {mp3_file}")
        return mp3_file
