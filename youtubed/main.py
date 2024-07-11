import os
import sys
import click
from typing import Callable

from .utils.process_playlist import process_playlist
from .utils.process_video import process_video
from .utils.help_box import help_box


def ensure_output_directory(path: str) -> None:
    """Create the output directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def get_processor(url: str) -> Callable:
    """Return the appropriate processor function based on the URL."""
    if url.startswith('https://www.youtube.com/playlist'):
        return process_playlist
    elif url.startswith('https://www.youtube.com/watch'):
        return process_video
    else:
        raise ValueError("Invalid URL. Please provide a valid YouTube video or playlist URL.")


@click.command()
@click.argument('url')
def youtubed(url: str) -> None:
    """Process YouTube videos or playlists."""
    output_base_path = 'data'
    ensure_output_directory(output_base_path)

    try:
        processor = get_processor(url)
        processor(url, output_base_path)
    except ValueError as e:
        click.echo(str(e), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    help_box()
    youtubed()