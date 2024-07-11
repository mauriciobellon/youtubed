import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

class TranscriptHandler:
    @staticmethod
    def get_transcript(video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
            return transcript
        except NoTranscriptFound as e:
            print(f"Erro ao obter a transcrição: {e}")
            return None

    @staticmethod
    def save_transcript_as_srt(transcript, output_file):
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as file:
                for i, entry in enumerate(transcript):
                    start = entry['start']
                    duration = entry.get('duration', 0)
                    end = start + duration
                    text = entry['text']
                    file.write(f"{i+1}\n")
                    file.write(f"{TranscriptHandler.format_time(start)} --> {TranscriptHandler.format_time(end)}\n")
                    file.write(f"{text}\n\n")
        except Exception as e:
            print(f"Erro ao salvar a transcrição: {e}")

    @staticmethod
    def format_time(seconds):
        millisec = int((seconds - int(seconds)) * 1000)
        seconds = int(seconds)
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02},{millisec:03}"
