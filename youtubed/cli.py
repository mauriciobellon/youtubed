import click
from .process_video import process_video
from .process_playlist import process_playlist

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

cli.add_command(video)

cli.add_command(playlist)

if __name__ == '__main__':
    cli()
