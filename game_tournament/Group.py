"""
Docstring for game_tournament.Group
"""
import random
from Team import Team
from game import Game
class Group:
    """ Group class represents a group in the tournament. It has a name and a list of teams. """
    def __init__(self, name):
        """ Custom constructor for Group class. """
        self.name = name
        self.teams = []
        self.games = []
    def add_team(self, team):
        """ Add a team to the group. """
        if isinstance(team, Team):
            self.teams.append(team)
        else:
            raise ValueError("Only Team objects can be added as a team.")
    def add_games(self):
        """ Add games for the group"""
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                game = Game(self.teams[i], self.teams[j])
                self.games.append(game)
    def __str__(self):
        """ String representation of the Group class. """
        return f"Group: {self.name}, Teams: {len(self.teams)}"
    def __repr__(self):
        """ String representation of the Group class. """
        return f"Group(name={self.name}, teams={repr(self.teams)})"
    def to_json(self):
        """ Convert the Group object to a JSON string. """
        return {
            "name": self.name,
            "teams": [team.to_json() for team in self.teams]
        }
    def display_group(self):
        """Display the teams in the group."""
        print(f"{self.name}:")
        for team in self.teams:
            print(f" - {team.name}")

    def display_games(self):
        """ Display the games in the group. """
        print(f"Group: {self.name}")
        for team in self.teams:
            print(f" {team}")
    def display_group_games(self):
        """ Display the games in the group. """
        print(f"Group: {self.name} ")
        for game in self.games:
            print(f" {game}")