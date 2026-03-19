from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import DirectoryTree
import os
from Tournament import Tournament
import random

class TextualUI(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #menu-container {
        width: 40;
        height: auto;
        border: thick $primary;
        padding: 1;
        background: $surface;
    }

    #tournament-scroll {
        padding: 2;
        border: solid $accent;
    }

    .title {
        text-align: center;
        width: 100%;
        text-style: bold;
        background: $primary;
        color: $text;
        margin-bottom: 1;
    }

    .header {
        text-style: bold underline;
        color: $secondary;
        margin-top: 1;
    }

    .subheader {
        text-style: italic;
        color: $accent;
    }

    #groups-scroll {
        padding: 2;
        border: solid $secondary;
    }

    #groups-scroll .subheader {
        background: $surface;
        color: $text;
        text-style: bold;
        padding-left: 2;
    }

    #games-scroll, #simulation-scroll {
        padding: 2;
    }

    .table-header {
        background: $surface;
        color: $text;
        text-style: bold;
        padding-left: 2;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }

    Static {
        margin-bottom: 0;
    }
    """

    BINDINGS = [
        ("l", "load", "[L]oad"),
        ("t", "display_tournament", "[T]ournament"),
        ("g", "display_groups", "[G]roups"),
        ("m", "display_games", "Ga[m]es"),
        ("p", "play", "[P]lay"),
        ("q", "exit_app", "[Q]uit"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def __init__(self):
        super().__init__()
        self.tournament = None  
        self.current_file = None
    
    def on_mount(self):
        self.query_one("#load").focus()
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="menu-container"):
            yield Button("Load Tournament", id="load")
            yield Button("Tournament", id="display")
            yield Button("Groups", id="groups")
            yield Button("Games", id="games")
            yield Button("Play", id="play")
            yield Button("Quit", id="exit")
        yield Footer()  
    def action_load(self):
        self.get_tournament_json()
    def action_display_tournament(self):
        self.display_tournament()
    def action_display_groups(self):
        self.display_groups()
    def action_display_games(self):
        self.display_games()
    def action_play(self):
        self.play_games()
    def action_quit(self):
        self.exit_app()
    def set_current_file(self, file_path:str):
        self.current_file = file_path
    def get_tournament_json(self):
        def on_file_selected(file_path: str | None) -> None:
            if file_path:
                self.current_file = file_path
                self.notify(f"Tournament file selected: {self.current_file}")
                self.open_tournament()
        self.push_screen(FileSelectorScreen(), callback=on_file_selected)
    def open_tournament(self):
        if self.current_file and os.path.exists(self.current_file):
            self.tournament = Tournament("Tournament")
            self.tournament.load_json(self.current_file)
            self.tournament.set_group_stage()
            self.notify(f"Tournament {self.tournament.name} loaded successfully")
        else:
            self.notify("No tournament file selected")
    def display_tournament(self):
        if self.tournament:
            self.notify("Here goes the tournament screen")
            self.push_screen(TournamentScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def display_groups(self):
        if self.tournament:
            self.notify("Here goes the groups screen")
            self.push_screen(GroupsScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def display_games(self):
        if self.tournament:
            self.notify("Here goes the games screen")
            self.push_screen(GamesScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def play_games(self):
        if self.tournament:
            self.push_screen(PlayGamesScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def exit_app(self):
        self.exit()
    def display_menu(self):
        self.run()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "load":
            self.get_tournament_json()
        elif button_id == "display":
            self.display_tournament()
        elif button_id == "groups":
            self.display_groups()
        elif button_id == "games":
            self.display_games()
        elif button_id == "play":
            self.play_games()
        elif button_id == "exit":
            self.exit_app()
class TournamentScreen(Screen):
    """Screen to display tournament details."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="tournament-scroll"):
            yield Static(f"Tournament: {self.tournament.name}", classes="title")
            
            yield Static("\nGroups", classes="header")
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="subheader")
                for team in group.teams:
                    yield Static(f"  • {team.name}")
            
            yield Static("\nGames", classes="header")
            # Checking both tournament.games and group games
            for group_name, group in self.tournament.groups.items():
                if group.games:
                    yield Static(f"\n{group_name} Games", classes="subheader")
                    for game in group.games:
                        yield Static(f"  - {game}")
            
            if self.tournament.games:
                yield Static("\nTournament Games", classes="subheader")
                for game in self.tournament.games:
                    yield Static(f"  - {game}")

        yield Footer()
class GroupsScreen(Screen):
    """Screen to display group details and standings."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="groups-scroll"):
            yield Static("Groups and Standings", classes="title")
            
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="header")
                
                # Table-like header for standings
                standings_header = f"{'Team':<15} {'Pts':>3} {'W':>2} {'L':>2} {'D':>2} {'GF':>3}:{'GA':<2} {'GD':>3}"
                yield Static(standings_header, classes="subheader")
                
                # Sort teams by points if standings are available
                sorted_standings = sorted(group.points.items(), key=lambda x: x[1]["points"], reverse=True)
                
                for team, stats in sorted_standings:
                    line = (f"{team.name[:15]:<15} {stats['points']:>3} {stats['wins']:>2} "
                            f"{stats['losses']:>2} {stats['draws']:>2} {stats['goals_for']:>3}:"
                            f"{stats['goals_against']:<2} {stats['goal_difference']:>3}")
                    yield Static(f"  {line}")
                    
        yield Footer()

class GamesScreen(Screen):
    """Screen to display all games."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="games-scroll"):
            yield Static("Tournament Games", classes="title")
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="header")
                for game in group.games:
                    yield Static(f"  - {game}")
            
            if self.tournament.games:
                yield Static("\nGeneral Games", classes="header")
                for game in self.tournament.games:
                    yield Static(f"  - {game}")
        yield Footer()

class PlayGamesScreen(Screen):
    """Screen to run simulation and display all results."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def on_mount(self) -> None:
        # We run the simulation when the screen is mounted
        # Note: play_games() has print statements, but we'll focus on displaying the state
        #self.tournament.play_games()
        for group in self.tournament.groups:
            self.tournament.groups[group].play_group_games()
        #self.tournament.display_games()
        #self.tournament.display_standings()
        self.tournament.set_knockout_stage()
        self.tournament.play_knockout_stage()
        self.tournament.play_final_stage()
        self.tournament.display_final_stage()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="simulation-scroll"):
            yield Static("Tournament Simulation Results", classes="title")
            
            # 1. Group Standings
            for group in self.tournament.groups:
                self.tournament.groups[group].play_group_games()    
            
            yield Static("\nGroup Stage Standings", classes="header")
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="subheader")
                standings_header = f"{'Team':<15} {'Pts':>3} {'W':>2} {'L':>2} {'D':>2} {'GF':>3}:{'GA':<2} {'GD':>3}"
                yield Static(standings_header, classes="table-header")
                
                sorted_standings = sorted(group.points.items(), key=lambda x: x[1]["points"], reverse=True)
                for team, stats in sorted_standings:
                    line = (f"{team.name[:15]:<15} {stats['points']:>3} {stats['wins']:>2} "
                            f"{stats['losses']:>2} {stats['draws']:>2} {stats['goals_for']:>3}:"
                            f"{stats['goals_against']:<2} {stats['goal_difference']:>3}")
                    yield Static(f"  {line}")

            # 2. Knockout Stage
            self.tournament.set_knockout_stage()
            if hasattr(self.tournament, 'set_knockout_stage'):
                yield Static("\nKnockout Stage", classes="header")
                for game in self.tournament.knockout_stage:
                    game.play()
                    if game.winner is None:
                        flip = random.randint(0, 1)
                        if flip == 0:
                            game.winner = game.team_a
                            game.loser = game.team_b
                        else:
                            game.winner = game.team_b
                            game.loser = game.team_a
                    result = f"Game: {game.team_a.name} {game.score.get(game.team_a.name, 0)} - {game.score.get(game.team_b.name, 0)} {game.team_b.name}"
                    winner = f"Winner: [bold green]{game.winner.name}[/bold green]" if game.winner else "TBD"
                    yield Static(f"\n  {result}")
                    yield Static(f"  {winner}")

                    

            # 3. Final Stage
            self.tournament.set_final_stage()   
            self.tournament.play_final_stage()
            if hasattr(self.tournament, 'set_final_stage'):
                yield Static("\nFinal Stage", classes="header")
                # Usually final_stage[0] is Final, final_stage[1] is 3rd place if logic follows
                for i, game in enumerate(self.tournament.final_stage):
                    label = "Final" if i == 0 else "Third Place"
                    result = f"{game.team_a.name} {game.score.get(game.team_a.name, 0)} - {game.score.get(game.team_b.name, 0)} {game.team_b.name}"
                    winner = f"{label} Winner: [bold gold1]{game.winner.name}[/bold gold1]" if game.winner else f"{label} TBD"
                    yield Static(f"\n  ({label}) {result}")
                    yield Static(f"  {winner}")

        yield Footer()

class FileSelectorScreen(Screen):
    def compose(self) -> ComposeResult:
        yield DirectoryTree("./")
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.dismiss(str(event.path))

if __name__ == "__main__":
    app = TextualUI()
    app.set_current_file("tournament.json")
    app.open_tournament()   
    app.run()
 

