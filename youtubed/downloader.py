import os
from yt_dlp import YoutubeDL

class Downloader:
    def __init__(self, output_path, cookie_file='cookies.txt'):
        self.output_path = output_path
        self.ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'cookiefile': cookie_file,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
            }
        }

    def download_video(self, url, playlist_title=None):
        # Define o caminho de salvamento do arquivo, incluindo o nome da playlist, se disponível
        self.ydl_opts['outtmpl'] = os.path.join(self.output_path, '%(uploader)s', '%(playlist_title)s', '%(title)s', '%(title)s.%(ext)s') if playlist_title else os.path.join(self.output_path, '%(uploader)s', '%(title)s', '%(title)s.%(ext)s')
        with YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            uploader = info_dict.get('uploader', 'UnknownUploader')
            # Pega o título da playlist, se disponível
            playlist_title = info_dict.get('playlist_title', playlist_title)
            filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp4').replace('.mkv', '.mp4')
        return filename, title, uploader, playlist_title

    def download_playlist(self, url):
        self.ydl_opts['extract_flat'] = True
        with YoutubeDL(self.ydl_opts) as ydl:
            playlist_dict = ydl.extract_info(url, download=False)
            playlist_title = playlist_dict.get('title', 'UnknownPlaylist')
            video_urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in playlist_dict['entries']]
        return video_urls, playlist_title
