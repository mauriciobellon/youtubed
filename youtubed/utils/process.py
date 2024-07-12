import asyncio
import aiohttp
import multiprocessing

from pathlib import Path
from typing import Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from pytube import YouTube
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound


BASE_DIR = Path("/home/mauricio/youtubed/")
DATA_DIR = BASE_DIR / "data"
MAX_WORKERS = multiprocessing.cpu_count()

def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_video_folder(channel_name: str, video_name: str) -> Path:
    return ensure_dir(DATA_DIR / channel_name / video_name)

async def get_names(url: str) -> Tuple[str, str]:
    try:
        yt = await asyncio.to_thread(YouTube, url)
        return yt.author, yt.title
    except Exception as e:
        print(f"An error occurred: {e}")
        return "", ""

class Downloader:
    def __init__(self, cookie_file: str = 'cookies.txt'):
        self.common_options = {
            'cookiefile': cookie_file,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
            }
        }
        self.video_options = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            **self.common_options
        }
        self.audio_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            **self.common_options
        }
        
    async def start(self, url: str, video_folder: Path) -> None:
        existing_files = set(file.name for file in video_folder.iterdir())
        tasks = []
        
        # Check and add video download task
        if not any(file.endswith('.mp4') for file in existing_files):
            tasks.append(self.download_video(url, video_folder))
        else:
            print("Video file already exists. Skipping video download.")
        
        # Check and add audio download task
        if not any(file.endswith('.mp3') for file in existing_files):
            tasks.append(self.download_audio(url, video_folder))
        else:
            print("Audio file already exists. Skipping audio download.")
        
        # Check and add transcript download task
        if not any(file.endswith('.srt') for file in existing_files):
            tasks.append(self.download_transcript(url, video_folder))
        else:
            print("Transcript file already exists. Skipping transcript download.")
        
        # Check and add thumbnail download task
        if not any(file.endswith('.jpg') for file in existing_files):
            tasks.append(self.download_thumbnail(url, video_folder))
        else:
            print("Thumbnail file already exists. Skipping thumbnail download.")
        
        # Check and add description download task
        if not any(file.endswith('.md') for file in existing_files):
            tasks.append(self.download_description(url, video_folder))
        else:
            print("Description file already exists. Skipping description download.")
        
        await asyncio.gather(*tasks)

    async def download_video(self, url: str, video_folder: Path) -> Dict[str, Any]:
        return await self._download_with_ydl(url, video_folder, self.video_options, "video")

    async def download_audio(self, url: str, video_folder: Path) -> Dict[str, Any]:
        try:          
            print("Downloading audio...")
            options = {
                **self.audio_options,
                'outtmpl': str(video_folder / '%(title)s.%(ext)s')
            }
            with YoutubeDL(options) as ydl:
                return await asyncio.to_thread(ydl.extract_info, url, download=True)
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return {}

    async def _download_with_ydl(self, url: str, video_folder: Path, options: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        try:
            print(f"Downloading {content_type}...")
            options['outtmpl'] = str(video_folder / '%(title)s.%(ext)s')
            with YoutubeDL(options) as ydl:
                return await asyncio.to_thread(ydl.extract_info, url, download=True)
        except Exception as e:
            print(f"Error downloading {content_type}: {e}")
            return {}

    async def download_transcript(self, url: str, video_folder: Path) -> None:
        try:
            print("Downloading transcript...")
            video_id = url.split("v=")[1]
            video_info = await self._get_video_info(url)
            video_title = video_info.get('title', video_id)
            output_file = video_folder / f"{video_title}.srt"

            if output_file.exists():
                print(f"Transcript already exists: {output_file}")
                return

            transcript = await asyncio.to_thread(
                YouTubeTranscriptApi.get_transcript,
                video_id,
                languages=['en', 'pt']
            )

            if not transcript:
                print("No transcript available.")
                return

            await self._write_transcript(output_file, transcript)
            print(f"Transcript saved to: {output_file}")

        except NoTranscriptFound:
            print(f"No transcript found for video: {video_id}")
        except Exception as e:
            print(f"Error downloading transcript: {e}")

    @staticmethod
    async def _write_transcript(output_file: Path, transcript: list) -> None:
        def write():
            with output_file.open('w', encoding='utf-8') as file:
                for i, entry in enumerate(transcript, 1):
                    start = entry['start']
                    duration = entry.get('duration', 0)
                    end = start + duration
                    text = entry['text']
                    file.write(f"{i}\n")
                    file.write(f"{Downloader._format_time(start)} --> {Downloader._format_time(end)}\n")
                    file.write(f"{text}\n\n")
        await asyncio.to_thread(write)

    @staticmethod
    def _format_time(seconds: float) -> str:
        millisec = int((seconds - int(seconds)) * 1000)
        seconds = int(seconds)
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02},{millisec:03}"

    async def download_thumbnail(self, url: str, video_folder: Path) -> Dict[str, Any]:
        try:
            print("Downloading thumbnail...")
            video_info = await self._get_video_info(url)
            thumbnail_url = video_info.get('thumbnail')
            video_title = video_info.get('title', 'video')
            
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail_url) as response:
                    if response.status == 200:
                        thumbnail_path = video_folder / f"{video_title}.jpg"
                        content = await response.read()
                        await asyncio.to_thread(thumbnail_path.write_bytes, content)
            
            return video_info
        except Exception as e:
            print(f"Error downloading thumbnail: {e}")
            return {}

    async def download_description(self, url: str, video_folder: Path) -> None:
        try:
            print("Downloading description...")
            video_info = await self._get_video_info(url)
            video_title = video_info.get('title', 'video')
            description = video_info.get('description', '')

            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            file_path = video_folder / f"{safe_title}.md"

            await self._write_description(file_path, video_title, description)
            print(f"Description saved to: {file_path}")

        except Exception as e:
            print(f"Error downloading description: {e}")

    @staticmethod
    async def _write_description(file_path: Path, title: str, description: str) -> None:
        def write():
            with file_path.open('w', encoding='utf-8') as file:
                file.write(f"# {title}\n\n")
                file.write(description)
        await asyncio.to_thread(write)

    async def _get_video_info(self, url: str) -> Dict[str, Any]:
        with YoutubeDL(self.video_options) as ydl:
            return await asyncio.to_thread(ydl.extract_info, url, download=False)


async def video_processor(url: str) -> None:
    downloader = Downloader()
    channel_name, video_name = await get_names(url)
    video_folder = get_video_folder(channel_name, video_name)
    await downloader.start(url, video_folder)


async def playlist_processor(url: str) -> None:
    print(f"Processing playlist: {url}")
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            playlist_info = await asyncio.to_thread(ydl.extract_info, url, download=False)
        
        if 'entries' not in playlist_info:
            print("Não foi possível encontrar vídeos na playlist.")
            return
        
        channel_name = playlist_info.get('channel', 'Unknown Channel')
        playlist_name = playlist_info.get('title', 'Unknown Playlist')
        video_titles = [entry['title'] for entry in playlist_info['entries']]
        
        # Create playlist markdown
        await create_playlist_markdown(channel_name, playlist_name, video_titles)
        
        async def process_video(entry):
            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
            print(f"Processando vídeo: {entry['title']}")
            await video_processor(video_url)
            print(f"Vídeo processado: {entry['title']}")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, asyncio.run, process_video(entry))
                for entry in playlist_info['entries']
            ]
            await asyncio.gather(*tasks)
        
        print("Processamento da playlist concluído.")
    
    except Exception as e:
        print(f"Erro ao processar a playlist: {e}")


async def create_playlist_markdown(channel_name: str, playlist_name: str, video_titles: list):
    playlist_folder = ensure_dir(DATA_DIR / channel_name / '_playlists')
    safe_playlist_name = "".join(c for c in playlist_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    markdown_path = playlist_folder / f"{safe_playlist_name}.md"
    
    content = f"# {playlist_name}\n\n"
    for i, title in enumerate(video_titles, 1):
        content += f"{i}. {title}\n"
    
    await asyncio.to_thread(markdown_path.write_text, content, encoding='utf-8')
    print(f"Playlist markdown created: {markdown_path}")


if __name__ == '__main__':
    asyncio.run(playlist_processor("https://www.youtube.com/playlist?list=PLKy51kKbOLly_Kld3JLKwphs0XsIWSkLk"))