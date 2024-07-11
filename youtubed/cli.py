# youtubed/cli.py

import click

@click.command()

def youtubed():
    click.echo("Running the youtubed command...")

if __name__ == "__main__":
    youtubed()