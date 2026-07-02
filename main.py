from quart.utils import cancel_tasks
from rich.box import Box
from textual.app import App, ComposeResult
from textual.widgets import Label, Static
from textual.screen import Screen
from textual import events
from textual.containers import Grid, Container, Horizontal
import textwrap
from dashboard_data import next_race_data, get_f1_news, current_standings

next_race_data = next_race_data()
news_list = get_f1_news()
current_standings = current_standings()

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

def format_name(category : str, index : int, parameter=None):
    base_name = current_standings[category][index]["name"]
    if category == "drivers":
        team = current_standings[category][index]["constructor"]
        return f"{base_name} ({team})"
    return base_name

def header():
    with Grid(id="header"):
        yield Label(ascii_art("logo.txt"), id="logo")
        yield Label("\nF1 [#E23E3C]CLI[/#E23E3C] [bold white on #141819]DASHBOARD[/bold white on #141819]\n   [gray]v0.1 \\[LIVE][/gray]",id="header-text")

def footer():
    with Container(id="footer"):
        yield Label("F1 CLI | CURRENT_RACE: $DAYS | PRESS \\[[#E23E3C]1-7[/#E23E3C]] FOR MENU | (q) QUIT",id="footer-text")

class Intro(Screen):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Label(ascii_art("logo.txt"), id="intro")
        yield Label("PRESS \\[ENTER] TO CONTINUE", id="hint")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.switch_screen(Dashboard())

class Dashboard(Screen):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("q", "quit_app", "Quits Application"),
        ("7", "Help_page", "moves to help page"),
    ]

    def action_Help_page(self) -> None:
        self.app.push_screen(Help_page())
    def action_quit_app(self) -> None:
        self.app.exit()

    def compose(self) -> ComposeResult:
        with Container(classes="dashboard-layout"):
            yield from header()

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
                    for news in news_list:
                        yield Label("\n"+ "[#E23E3C]-  [/#E23E3C]" + news + "[#E23E3C].[/#E23E3C]")

            with Grid(id="second-grid"):
                with box(f"NEXT RACE: [white on #141819]{next_race_data['country']} GRAND PRIX[/white on #141819] ({next_race_data['location']})"):
                    yield Label(f"   Date : {next_race_data['weekend_duration']}.\n   Status :[yellow] RACE STARTS in {next_race_data['race']['time_left']['days']} days, {next_race_data['race']['time_left']['hours']} hours, {next_race_data['race']['time_left']['minutes']} min[/yellow]\n")
                    text = textwrap.dedent(
                        f"""\
                        ⏱️ [#E23E3C]WEEKEND TIMETABLE[/#E23E3C]
                            FP1   : {next_race_data["fp"]["fp_dates"]["fp1_date"]} ({next_race_data["fp"]["fp_times"]["fp1_time"]} CET)
                            FP2   : {next_race_data["fp"]["fp_dates"]["fp2_date"]} ({next_race_data["fp"]["fp_times"]["fp2_time"]} CET)
                            FP3   : {next_race_data["fp"]["fp_dates"]["fp3_date"]} ({next_race_data["fp"]["fp_times"]["fp3_time"]} CET)
                            Quali : {next_race_data["quali"]["quali_date"]} ({next_race_data["quali"]["quali_time"]} CET)
                            Race  : {next_race_data["race"]["race_date"]} ({next_race_data["race"]["race_time"]} CET)
                        """
                    )
                    yield Label(text)
                with box("LIVE STANDINGS"):
                    standings = textwrap.dedent(
                        f"""\
                        DRIVERS:
                        [#E23E3C]1.[/#E23E3C] {format_name("drivers", 0):<25} {current_standings["drivers"][0]["points"]:>3} [yellow]Points[/yellow] ({current_standings["drivers"][0]["wins"]} wins)
                        [#E23E3C]2.[/#E23E3C] {format_name("drivers", 1):<25} {current_standings["drivers"][1]["points"]:>3} [yellow]Points[/yellow] ({current_standings["drivers"][1]["wins"]} wins)
                        [#E23E3C]3.[/#E23E3C] {format_name("drivers", 2):<25} {current_standings["drivers"][2]["points"]:>3} [yellow]Points[/yellow] ({current_standings["drivers"][2]["wins"]} wins)     
                        CONSTRUCTORS
                        [#E23E3C]1.[/#E23E3C] {format_name("constructors", 0):<21}     {current_standings["constructors"][0]["points"]} [yellow]Points[/yellow] ({current_standings["constructors"][0]["wins"]} wins)
                        [#E23E3C]2.[/#E23E3C] {format_name("constructors", 1):<21}     {current_standings["constructors"][1]["points"]} [yellow]Points[/yellow] ({current_standings["constructors"][1]["wins"]} wins)
                        [#E23E3C]3.[/#E23E3C] {format_name("constructors", 2):<21}     {current_standings["constructors"][2]["points"]} [yellow]Points[/yellow] ({current_standings["constructors"][2]["wins"]} wins)
                        """
                    )
                    yield Label(standings)

            yield from footer()

class Help_page(Screen):
    CSS_PATH = "style.tcss"
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        with Container(classes="help-layout"):
            yield from header()
            with Container(id="help-container"):
                help_text = """"""
                yield Label("HELP PAGE")
            yield from footer()

class F1App(App):
    def on_mount(self) -> None:
        self.push_screen(Intro())

if __name__ == "__main__":
    F1App().run()