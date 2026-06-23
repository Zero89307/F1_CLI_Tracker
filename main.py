from rich.box import Box
from textual.app import App, ComposeResult
from textual.widgets import Label, Static
from textual.screen import Screen
from textual import events
from textual.containers import Grid, Container, Horizontal
import textwrap

def ascii_art(filename : str):
    try:
        with open("ascii arts/" + filename) as file:
            return str(file.read())
    except FileNotFoundError:
        return "ASCII ART NOT FOUND"
def box(text: str):
    bento = Static(classes="bento-box")
    bento.border_title = f"[#E23E3C]{text}[/#E23E3C]"
    return bento
class Intro(Screen):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Label(ascii_art("logo.txt"), id="intro")
        yield Label("PRESS \\[ENTER] TO CONTINUE", id="hint")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.push_screen(Dashboard())

class Dashboard(Screen):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("q", "quit_app", "Quits Application"),
    ]

    def action_quit_app(self) -> None:
        self.app.exit()

    def compose(self) -> ComposeResult:
        with Grid(id="header"):
            yield Label(ascii_art("logo.txt"), id="logo")
            yield Label("\nF1 [#E23E3C]CLI[/#E23E3C] [bold white on #141819]DASHBOARD[/bold white on #141819]\n   [gray]v0.1 \\[LIVE][/gray]", id="header-text")

        with Grid(id="first-grid"):
            with box("MAIN MENU"):
                menu = textwrap.dedent("""
                  [yellow][1][/yellow] Session Overview
                  [yellow][2][/yellow] Race Calender
                  [yellow][3][/yellow] Driver Standings
                  [yellow][4][/yellow] Constructors Standings
                  [yellow][5][/yellow] Current Weekend
                  [yellow][6][/yellow] News
                  [yellow][7][/yellow] Help / Info 

                """)
                yield Label(menu)
            yield box("NEWS")
        with Grid(id="second-grid"):
            with box("NEXT RACE: [white on #141819]COUNTRY GRAND PRIX[/white on #141819]"):
                yield Label(f"   Date : 1. - 3. January 0000\n   Status : [yellow]Upcoming[/yellow] [#E8D9BF](RACE STARTS in $DAYS, $HOURS)[/#E8D9BF]\n")
                text = textwrap.dedent(
                    f"""\
                    ⏱️ [#E23E3C]WEEKEND TIMETABLE[/#E23E3C]
                        FP1   : MON 1.01 (0.00 CET)
                        FP2   : MON 1.01 (0.00 CET)
                        FP3   : MON 1.01 (0.00 CET)
                        Quali : MON 1.01 (0.00 CET)
                        Race  : MON 1.01 (0.00 CET)
                    """
                )
                yield Label(text)
            yield box("LIVE STANDINGS")

        with Container(id="footer"):
            yield Label("F1 CLI | CURRENT_RACE: $DAYS | PRESS \\[[#E23E3C]1-7[/#E23E3C]] FOR MENU | (q) QUIT", id="footer-text")


class F1App(App):
    def on_mount(self) -> None:
        self.push_screen(Intro())

if __name__ == "__main__":
    F1App().run()