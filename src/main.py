from __future__ import annotations
import os
from PyInquirer import prompt
from rich.console import Console
import click
from click_shell import shell
from src.streamer import AnimeStreamer

streamer = AnimeStreamer()
console = Console()


@shell(prompt="AnimeStreamer >> ")
def cli():
    console.print("Type 'help' to show commands")


@cli.command()
@click.option("-q", "--query", required=True, help="Anime to search for.")
def find(query: str):
    streamer.search("".join(query))
    streamer.sort_results(key="seeders", reverse=True)
    console.print("You can type 'show [-p page_num]'")


@cli.command()
def sort():
    questions = [
        {
            "type": "list",
            "name": "key",
            "message": "Sort by?",
            "choices": ["seeders", "date", "size", "completed_downloads", "leechers"],
            "filter": lambda val: val.lower()
        },
        {
            "type": "list",
            "name": "order",
            "message": "Ascending/Descending?",
            "choices": ["ascending", "descending"],
            "filter": lambda val: val.lower()
        }
    ]
    answers = prompt(questions)
    key, order = answers.values()
    streamer.sort_results(key, reverse=order == "descending")


@cli.command()
@click.option("-p", "--page", default=1, help="Page number to show.")
def show(page: int):
    streamer.set_page(page)
    streamer.list_top_results()


@cli.command()
@click.option("-t", "--torrent", required=True, type=click.INT, help="Torrent to play.")
def play(torrent: int):
    streamer.play_torrent(torrent)


@cli.command()
@click.option("-p", "--path", type=click.Path(exists=True), help="Path for downloading torrents.")
def path(path):
    if path is None:
        console.print(streamer.get_download_path())
    else:
        streamer.set_download_path(path)
        console.print("Path set")


@cli.command()
def clear():
    """Clears console."""
    os.system("cls||clear")


if __name__ == "__main__":
    cli()