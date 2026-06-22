from textual.app import App, ComposeResult
from textual.widgets import Label, Static
from textual.screen import Screen
from textual import events
from textual.containers import Grid, Container, Horizontal

def ascii_art(filename : str):
    try:
        with open("ascii arts/" + filename) as file:
            return str(file.read())
    except FileNotFoundError:
        return "ASCII ART NOT FOUND"

class Intro(Screen):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Label(ascii_art("logo.txt"), id="intro")
        yield Label("PRESS \\[ENTER] TO CONTINUE", id="hint")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.exit()

class Dashboard(Screen):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        with Grid(id="header"):
            yield Label(ascii_art("logo.txt"), id="logo")
            yield Label("\nF1 CLI DASHBOARD", id = "header-text")

        with Grid(id="first-grid"):
            yield Static(classes="bento-box")
            yield Static(classes="bento-box")
        with Grid(id="second-grid"):
            yield Static(classes="bento-box")
            yield Static(classes="bento-box")

        with Container(id="footer"):
            yield Label("F1 CLI | CURRENT_RACE: $DAYS | PRESS \\[1-7] FOR MENU | (q) QUIT", id="footer-text")


class F1App(App):
    def on_mount(self) -> None:
        self.push_screen(Dashboard())

if __name__ == "__main__":
    F1App().run()