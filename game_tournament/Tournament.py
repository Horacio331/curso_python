"""
Docstring for game_tournament.Tournament
"""
import random
import json
from Game import Game
from Team import Team
from Sport import Sport
from Athlete import Athlete
from Group import Group

class Tournament:
    """ Tournament class represents a tournament. It has a name, a list of games, and a list of teams. """
    def __init__(self, name):
        """ Custom constructor for Tournament class. """
        self.name = name
        self.games = []
        self.teams = []
        self.groups = {}
    def add_team(self, team):
        """ Add a team to the tournament. """
        if isinstance(team, Team):
            self.teams.append(team)
        else:
            raise ValueError("Only Team objects can be added as a team.")
    def add_game(self, game):
        """ Add a game to the tournament. """
        if isinstance(game, Game):
            self.games.append(game)
        else:
            raise ValueError("Only Game objects can be added as a game.") 
    def __str__(self):
        """ String representation of the Tournament class. """
        return f"Tournament: {self.name}, Teams: {len(self.teams)}, Games: {len(self.games)}"
    def __repr__(self):
        """ String representation of the Tournament class. """
        return f"Tournament(name={self.name}, teams={repr(self.teams)}, games={repr(self.games)})"
    def to_json(self):
        """ Convert the Tournament object to a JSON string. """
        return {
            "name": self.name,
            "teams": [team.to_json() for team in self.teams],
            "games": [game.to_json() for game in self.games]
        }
    def set_group(self, group_list, group_name):
        """ Set the group for each team in the tournament. """
        group = Group(group_name)
        for team in group_list:
            group.add_team(team)
        group.add_games()
        self.groups[group_name] = group
    def set_group_stage(self):
        """ Set the group stage """
        if len(self.teams) == 8:
            # Create two groups of 4 teams each
            group_a = self.teams[:4]
            group_b = self.teams[4:]
            # Create games for group A
            self.set_group(group_a, "Group A")
            # Create games for group B
            self.set_group(group_b, "Group B")
    def load_json(self, filename):
        """ Load a Tournament object from a JSON file."""
        print("Tournament")
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for team_data in data:
                team_name = team_data["name"]
                sport_name = team_data["sport"]["name"]
                sport_league = team_data["sport"]["league"]
                sport_num_players = team_data["sport"]["num_players"]
                sport = Sport(sport_name, sport_num_players, sport_league)
                team = Team(team_name, sport)
                players = team_data["athletes"]
                for player in players:
                    team.add_athlete(Athlete(player))
                self.add_team(team)
    def display_tournament(self):
        """ Display the tournament. """
        print(f"Tournament: {self.name}")
        for group in self.groups:
            self.groups[group].display_group()
        self.display_games()
    def display_games(self):
        """ Display the games. """
        for group in self.groups:
            self.groups[group].display_group_games()
    def play_games(self):
        """ Play the games. """
        for group in self.groups:
            self.groups[group].play_group_games()
        self.display_games()
        self.display_standings()
        self.set_knockout_stage()
        self.play_knockout_stage()
        self.play_final_stage()
        self.display_final_stage()
    def display_standings(self):
        """ Display the standings of the tournament. """
        for group in self.groups:
            self.groups[group].display_standings()
    def get_qualified_teams(self):
        """ Get the qualified teams for the next stage. """
        qualified_teams = []
        for group in self.groups:
            qualified_teams.append(self.groups[group].get_qualified_teams())
        return qualified_teams
    def set_knockout_stage(self):
        """ Set the knockout stage """
        qualified_teams = self.get_qualified_teams()
        self.knockout_stage = []
        g1 = Game(qualified_teams[0][0],qualified_teams[1][1])
        g2 = Game(qualified_teams[0][1],qualified_teams[1][0])
        self.knockout_stage.append(g1)
        self.knockout_stage.append(g2)
        print(self.knockout_stage)
    def play_knockout_stage(self):
        """ Play the knockout stage """
        for game in self.knockout_stage:
            game.play()
            if game.winner is None:
                flip = random.randint(0, 1)
                if flip == 0:
                    game.winner = game.team_a
                    game.loser = game.team_b
                else:
                    game.winner = game.team_b
                    game.loser = game.team_a
        self.display_knockout_stage()
        self.set_final_stage()
    def display_knockout_stage(self):
        """ Display the knockout stage """
        print("Knockout Stage")
        for game in self.knockout_stage:
            print(game)
    def set_final_stage(self):
        """ Set the final stage """
        self.final_stage = []
        g1 = Game(self.knockout_stage[0].winner,self.knockout_stage[1].winner)
        g3 = Game(self.knockout_stage[0].loser,self.knockout_stage[1].loser)
        self.final_stage.append(g1)
        self.final_stage.append(g3)
    def play_final_stage(self):
        """ Play the final stage """
        for game in self.final_stage:
            game.play()
    def display_final_stage(self):
        """ Display the final stage """
        print("Final Stage")
        for game in self.final_stage:
            print(game)
    
if __name__ == "__main__":
    tournament = Tournament("FIFA World Cup")
    tournament.load_json("tournament.json")
    tournament.set_group_stage()
    tournament.display_tournament()
   # tournament.set_games()
    tournament.display_games()
    #print(tournament.groups['Group A'].games)
    #print(tournament.groups['Group B'].games)
   # print(tournament)