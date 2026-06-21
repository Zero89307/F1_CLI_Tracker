from textual.app import App, ComposeResult
from textual.widgets import Label, Static
from textual.screen import Screen
from textual import events

def ascii_art(filename : str):
    try:
        with open("ascii arts/" + filename) as file:
            return str(file.read())
    except FileNotFoundError:
        return "ASCII ART NOT FOUND"

class Intro(Screen):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Label(ascii_art("intro.txt"), id="intro")
        yield Label("PRESS \\[ENTER] TO CONTINUE", id="hint")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.exit()

class F1App(App):
    def on_mount(self) -> None:
        self.push_screen(Intro())

if __name__ == "__main__":
    F1App().run()