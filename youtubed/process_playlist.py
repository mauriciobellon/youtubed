from concurrent.futures import ThreadPoolExecutor, as_completed
from .downloader import Downloader
from .process_video import process_video


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