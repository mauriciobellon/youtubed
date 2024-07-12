import sys
import click
import asyncio
from typing import Callable, Coroutine

from .utils.process import playlist_processor
from .utils.process import video_processor
from .utils.help_box import help_box


def get_processor(url: str) -> Coroutine:
    if url.startswith('https://www.youtube.com/playlist'):
        return playlist_processor(url)
    elif url.startswith('https://www.youtube.com/watch'):
        return video_processor(url)
    else:
        raise ValueError("Invalid URL. Please provide a valid YouTube video or playlist URL.")


@click.command()
@click.argument('url')
def youtubed(url: str) -> None:
    try:
        coroutine = get_processor(url)
        asyncio.run(coroutine)
    except ValueError as e:
        click.echo(str(e), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    help_box()