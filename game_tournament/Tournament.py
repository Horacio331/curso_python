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
        for group in self.groups:
            self.groups[group].display_group_games()

if __name__ == "__main__":
    tournament = Tournament("FIFA World Cup")
    tournament.load_json("tournament.json")
    tournament.set_group_stage()
    tournament.display_tournament()
    #print(tournament.groups['Group A'].games)
    #print(tournament.groups['Group B'].games)
   # print(tournament)