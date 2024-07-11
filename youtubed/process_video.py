import os
from .downloader import Downloader
from .audio_extractor import AudioExtractor
from .transcript_handler import TranscriptHandler


def process_video(url, output_base_path, playlist_title=None):
    try:
        downloader = Downloader(output_base_path)
        video_file, title, uploader, playlist_title = downloader.download_video(url, playlist_title)
        print(f"Vídeo MP4 baixado e salvo em: {video_file}")

        AudioExtractor.extract_audio(video_file)
        video_folder = os.path.dirname(video_file)
        srt_file = os.path.join(video_folder, title + '.srt')
        if not os.path.exists(srt_file):
            video_id = url.split("v=")[1]
            transcript = TranscriptHandler.get_transcript(video_id)
            if transcript:
                TranscriptHandler.save_transcript_as_srt(transcript, srt_file)
                print(f"Legenda salva em: {srt_file}")
            else:
                print("Não foi possível obter a transcrição.")
        else:
            print(f"Legenda já existe: {srt_file}")
        
    except Exception as e:
        print(f"Erro ao processar o vídeo: {e}")