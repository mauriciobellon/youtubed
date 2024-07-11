import os
import click


@click.command()
@click.argument('url')
def youtubed(url):

    output_base_path = 'data'
    
    if not os.path.exists(output_base_path):
        os.makedirs(output_base_path)

    if url.startswith('https://www.youtube.com/playlist'):
        from .utils.process_playlist import process_playlist
        process_playlist(url, output_base_path)

    elif url.startswith('https://www.youtube.com/watch'):
        from .utils.process_video import process_video
        process_video(url, output_base_path)

    else:
        print("URL inválida.")
        exit(1)


if __name__ == '__main__':
    from utils.help_box import help_box
    help_box()