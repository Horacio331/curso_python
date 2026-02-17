"""
Docstring for game_tournament.Game
Game class represents a game in the tournament. It has a name, a sport, and a list of teams.
"""
import random
import json
from Team import Team
from Sport import Sport
from Athlete import Athlete


class Game:
    """ Game class represents a game in the tournament. It has two teams and a score"""

    def __init__(self, A: Team, B: Team):
        """ Custom constructor for Game class. """
        self.set_team(A, "local")
        self.set_team(B, "visitor")
        self.score = {
            A.name: 0, B.name: 0
        }

    def set_team(self, team, role):
        """ Set a team for the game. """
        if isinstance(team, Team):
            if role == "local":
                self.team_a = team
            elif role == "visitor":
                self.team_b = team
            else:
                raise ValueError("Role must be 'local' or 'visitor'.")
        else:
            raise ValueError("Only Team objects can be set as a team.")

    def play(self):
        """ Simulate playing the game by randomly assigning scores to each team. """
        self.score[self.team_a.name] = random.randint(
            0, Sport.max_score[self.team_a.sport.name])
        self.score[self.team_b.name] = random.randint(
            0, Sport.max_score[self.team_b.sport.name])

    def __str__(self):
        """ String representation of the Game class. """
        a = self.score[self.team_a.name]
        b = self.score[self.team_b.name]
        return f"{self.team_a.name} vs {self.team_b.name} - Score: {a}:{b}"

    def __repr__(self):
        """ String representation of the Game class. """
        return f"Game(team_a={repr(self.team_a)}, team_b={repr(self.team_b)}, score={self.score})"

    def to_json(self):
        """ Convert the Game object to a JSON string. """
        return {
            "team_a": self.team_a.to_json(),
            "team_b": self.team_b.to_json(),
            "score": self.score
        }


def a_game():
    """ Example usage of the Game class. """
    players_mex = ['Chicharito', 'Piojo', 'Guardado',
                   'Hector Moreno',
                   'Rafa Marquez', 'Salcido', 'Vela', 'Dos Santos', 'Herrera', 'Layun', 'Corona']
    players_arg = ['Messi', 'Di Maria',
                   'Aguero', 'Higuain',
                   'Mascherano',
                   'Biglia', 'Dybala', 'Paredes', 'Tagliafico', 'Otamendi', 'Zabaleta']
    sport = Sport("Futbol", 11, "FIFA")
    team_mex = Team("Mexico", sport)
    team_arg = Team("Argentina", sport)
    for player in players_mex:
        team_mex.add_athlete(Athlete(player))
    for player in players_arg:
        team_arg.add_athlete(Athlete(player))
    game = Game(team_mex, team_arg)
    game_string = game.to_json()
    return game_string


def save_game_to_json(game_data, filename):
    """ Save the game object to a JSON file. """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(game_data, f, indent=4)


def a_tournament():
    """ Example usage of the Game class. """
    players_mex = ['Chicharito', 'Piojo', 'Guardado', 'Hector Moreno',
                   'Rafa Marquez', 'Salcido', 'Vela', 'Dos Santos', 'Herrera', 'Layun', 'Corona']
    players_arg = ['Messi', 'Di Maria', 'Aguero', 'Higuain', 'Mascherano',
                   'Biglia', 'Dybala', 'Paredes', 'Tagliafico', 'Otamendi', 'Zabaleta']
    players_peru = ['Guerrero', 'Carrillo', 'Flores', 'Yotun', 'Cueva',
                    'Tapia', 'Advincula', 'Trauco', 'Araujo', 'Garcia', 'Gallese']
    players_france = ['Mbappe', 'Griezmann', 'Pogba', 'Kante', 'Varane',
                      'Lloris', 'Hernandez', 'Pavard', 'Matuidi', 'Dembele', 'Coman']
    players_spain = ['Ramos', 'Iniesta', 'Xavi', 'Pique', 'Busquets',
                     'Alba', 'Isco', 'Morata', 'Silva', 'Asensio', 'De Gea']
    players_brazil = ['Neymar', 'Coutinho',
                      'Firmino',
                      'Casemiro', 'Alisson',
                      'Thiago Silva', 'Marquinhos',
                      'Willian', 'Gabriel Jesus', 'Fernandinho', 'Danilo']
    players_italia = ['Buffon', 'Chiellini', 'Bonucci', 'Donnarumma', 'Insigne',
                      'Bernardeschi', 'Verratti', 'Jorginho', 'Chiesa', 'Belotti', 'Immobile']
    players_japan = ['Kagawa', 'Honda', 'Okazaki', 'Nagatomo', 'Yoshida',
                     'Hasebe', 'Inui', 'Shibasaki', 'Kawashima', 'Muto', 'Osako']
    sport = Sport("Futbol", 11, "FIFA")
    team_mex = Team("Mexico", sport)
    team_arg = Team("Argentina", sport)
    team_peru = Team("Peru", sport)
    team_france = Team("France", sport)
    team_spain = Team("Spain", sport)
    team_brazil = Team("Brazil", sport)
    team_italia = Team("Italia", sport)
    team_japan = Team("Japan", sport)
    for player in players_mex:
        team_mex.add_athlete(Athlete(player))
    for player in players_arg:
        team_arg.add_athlete(Athlete(player))
    for player in players_peru:
        team_peru.add_athlete(Athlete(player))
    for player in players_france:
        team_france.add_athlete(Athlete(player))
    for player in players_spain:
        team_spain.add_athlete(Athlete(player))
    for player in players_brazil:
        team_brazil.add_athlete(Athlete(player))
    for player in players_italia:
        team_italia.add_athlete(Athlete(player))
    for player in players_japan:
        team_japan.add_athlete(Athlete(player))
    tournament_list = [team_mex, team_arg,
                       team_peru, team_france,
                       team_spain, team_brazil, team_italia, team_japan]
    json_string = ""
    for team in tournament_list:
        json_string += f"{team.to_json()}\n"
    return json_string


if __name__ == "__main__":
    string_game = a_tournament()
    save_game_to_json(string_game, "tournament.json")
    print(string_game)