import click
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .downloader import Downloader
from .audio_extractor import AudioExtractor
from .transcript_handler import TranscriptHandler

@click.group()
def cli():
    pass

@click.command()
@click.argument('url')
def video(url):
    output_base_path = 'data/youtube'
    process_video(url, output_base_path)

@click.command()
@click.argument('url')
def playlist(url):
    output_base_path = 'data/youtube'
    process_playlist(url, output_base_path)

def process_video(url, output_base_path, playlist_title=None):
    try:
        downloader = Downloader(output_base_path)
        video_file, title, uploader, playlist_title = downloader.download_video(url, playlist_title)
        print(f"Vídeo MP4 baixado e salvo em: {video_file}")
        
        mp3_file = AudioExtractor.extract_audio(video_file)
        
        # Salvando a legenda na mesma pasta que os arquivos de vídeo e áudio
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

def process_playlist(url, output_base_path):
    downloader = Downloader(output_base_path)
    video_urls, playlist_title = downloader.download_playlist(url)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_video, video_url, output_base_path, playlist_title) for video_url in video_urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Erro ao processar o vídeo: {e}")

cli.add_command(video)
cli.add_command(playlist)

if __name__ == '__main__':
    cli()
