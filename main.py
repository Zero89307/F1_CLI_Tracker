from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label, Button
from textual.screen import Screen
from textual import events

class Intro(Screen):
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        yield Label("F1 CLI 2026", id="intro")
        yield Label("PRESS [ENTER] TO CONTINUE", id="hint")

    def on_key(self, event: events.KeyEvent) -> None:
        if event.key == "enter":
            self.app.exit()

class F1App(App):
    def on_mount(self) -> None:
        self.push_screen(Intro())

if __name__ == "__main__":
    F1App().run()