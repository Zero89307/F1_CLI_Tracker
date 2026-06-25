from rich.box import Box
from textual.app import App, ComposeResult
from textual.widgets import Label, Static
from textual.screen import Screen
from textual import events
from textual.containers import Grid, Container, Horizontal
import textwrap
from dashboard_data import next_race_data

next_race_data = next_race_data()

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
            with box("NEWS"):
                news = textwrap.dedent(
                f"""\
                [#E23E3C]CURRENT NEWS:[/#E23E3C]
                
                NEWS PULLED FROM API NEWS PULLED FROM API NEWS PULLED FROM API NEWS PULLED FROM API
                NEWS PULLED FROM API NEWS PULLED FROM API NEWS PULLED FROM API NEWS PULLED FROM API
                NEWS PULLED FROM API NEWS PULLED FROM API NEWS PULLED FROM API NEWS PULLED FROM API
                """
                )
                yield Label(news)

        with Grid(id="second-grid"):
            with box(f"NEXT RACE: [white on #141819]{next_race_data["country"]} GRAND PRIX[/white on #141819] ({next_race_data["location"]})"):
                yield Label(f"   Date : {next_race_data["weekend_duration"]}.\n   Status :[yellow] RACE STARTS in {next_race_data["race"]["time_left"]["days"]} days, {next_race_data["race"]["time_left"]["hours"]} hours, {next_race_data["race"]["time_left"]["minutes"]} min[/yellow]\n")
                text = textwrap.dedent(
                    f"""\
                    ⏱️ [#E23E3C]WEEKEND TIMETABLE[/#E23E3C]
                        FP1   : MON {next_race_data["fp"]["fp_dates"]["fp1_date"]} ({next_race_data["fp"]["fp_times"]["fp1_time"]} CET)
                        FP2   : MON {next_race_data["fp"]["fp_dates"]["fp2_date"]} ({next_race_data["fp"]["fp_times"]["fp2_time"]} CET)
                        FP3   : MON {next_race_data["fp"]["fp_dates"]["fp3_date"]} ({next_race_data["fp"]["fp_times"]["fp3_time"]} CET)
                        Quali : MON {next_race_data["quali"]["quali_date"]} ({next_race_data["quali"]["quali_time"]} CET)
                        Race  : MON {next_race_data["race"]["race_date"]} ({next_race_data["race"]["race_time"]} CET)
                    """
                )
                yield Label(text)
            with box("LIVE STANDINGS"):
                standings = textwrap.dedent(
                    f"""\
                    DRIVERS:
                    1. $DRIVER_NAME     $DRIVER_POINTS ($DRIVER_WINS)
                    2. $DRIVER_NAME     $DRIVER_POINTS ($DRIVER_WINS)
                    3. $DRIVER_NAME     $DRIVER_POINTS ($DRIVER_WINS)               
                    CONSTRUCTORS:
                    1. $CONSTRUCTORS_NAME     $CONSTRUCTORS_POINTS
                    2. $CONSTRUCTORS_NAME     $CONSTRUCTORS_POINTS
                    3. $CONSTRUCTORS_NAME     $CONSTRUCTORS_POINTS
                    """
                )
                yield Label(standings)

        with Container(id="footer"):
            yield Label("F1 CLI | CURRENT_RACE: $DAYS | PRESS \\[[#E23E3C]1-7[/#E23E3C]] FOR MENU | (q) QUIT", id="footer-text")


class F1App(App):
    def on_mount(self) -> None:
        self.push_screen(Intro())

if __name__ == "__main__":
    F1App().run()