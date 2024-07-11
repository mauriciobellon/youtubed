import click
from help_box import help_box

output_base_path = 'data/donwloads'

@click.command()
@click.argument('url')
def youtubed(url):
    
    if url.startswith('https://www.youtube.com/playlist'):
        from .process_playlist import process_playlist
        process_playlist(url, output_base_path)

    elif url.startswith('https://www.youtube.com/watch'):
        from .process_video import process_video
        process_video(url, output_base_path)

    else:
        print("URL inválida.")
        exit(1)


if __name__ == '__main__':
    help_box()