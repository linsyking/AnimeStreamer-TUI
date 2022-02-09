﻿from rich.panel import Panel
from textual.reactive import Reactive

from animestreamer import streamer
from animestreamer.widgets import CustomWidget


class TorrentResults(CustomWidget):
    selected_torrent = Reactive(1)

    def render(self):
        if streamer.results:
            page = f"{streamer.curr_page + 1}/{streamer.get_page_count() + 1}"
        else:
            page = "No results"
        return Panel(
            streamer.get_results_table(selected=self.selected_torrent),
            title=f"Torrents [yellow][{page}][/yellow]",
            **self.get_style()
        )

    def play_torrent(self):
        torrent_num = self.selected_torrent + (streamer.curr_page * streamer.show_at_once)
        streamer.play_torrent(torrent_num)

    def next_torrent(self):
        if self.selected_torrent < streamer.show_at_once:
            self.selected_torrent += 1

    def prev_torrent(self):
        if self.selected_torrent > 1:
            self.selected_torrent -= 1

    def next_page(self):
        streamer.next_page()
        self.refresh()

    def prev_page(self):
        streamer.prev_page()
        self.refresh()