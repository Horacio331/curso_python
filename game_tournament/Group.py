"""
Docstring for game_tournament.Group
"""
import random
from Team import Team
from Game import Game

class Group:
    """ Group class represents a group in the tournament. It has a name and a list of teams. """
    def __init__(self, name):
        """ Custom constructor for Group class. """
        self.name = name
        self.teams = []
        self.games = []
        self.points = {}
    def add_team(self, team):
        """ Add a team to the group. """
        if isinstance(team, Team):
            self.teams.append(team)
            self.points[team] = {"points": 0, "wins": 0, "losses": 0, "draws": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0} # win = 3 points, draw = 1 point, loss = 0 points
        else:
            raise ValueError("Only Team objects can be added as a team.")
    def add_games(self):
        """ Add games for the group. """
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
        """ Display the group. """
        print(f"Group: {self.name}")
        for team in self.teams:
            print(f"  {team}")
    def display_group_games(self):
        """ Display the group games. """
        print(f"Group: {self.name}")
        for game in self.games:
            print(f"  {game}")
    def play_group_games(self):
        """ Play the group games. """
        for game in self.games:
            game.play()
            if game.score[game.team_a.name] > game.score[game.team_b.name]:
                self.points[game.team_a]["points"] += 3
                self.points[game.team_a]["wins"] += 1
                self.points[game.team_b]["losses"] += 1
                self.points[game.team_a]["goals_for"] += game.score[game.team_a.name]
                self.points[game.team_a]["goals_against"] += game.score[game.team_b.name]
                self.points[game.team_b]["goals_for"] += game.score[game.team_b.name]
                self.points[game.team_b]["goals_against"] += game.score[game.team_a.name]
                self.points[game.team_a]["goal_difference"] += game.score[game.team_a.name] - game.score[game.team_b.name]
                self.points[game.team_b]["goal_difference"] += game.score[game.team_b.name] - game.score[game.team_a.name]
            elif game.score[game.team_a.name] < game.score[game.team_b.name]:
                self.points[game.team_b]["points"] += 3
                self.points[game.team_b]["wins"] += 1
                self.points[game.team_a]["losses"] += 1
                self.points[game.team_b]["goals_for"] += game.score[game.team_b.name]
                self.points[game.team_b]["goals_against"] += game.score[game.team_a.name]
                self.points[game.team_a]["goals_for"] += game.score[game.team_a.name]
                self.points[game.team_a]["goals_against"] += game.score[game.team_b.name]
                self.points[game.team_b]["goal_difference"] += game.score[game.team_b.name] - game.score[game.team_a.name]
                self.points[game.team_a]["goal_difference"] += game.score[game.team_a.name] - game.score[game.team_b.name]
            else:
                self.points[game.team_a]["points"] += 1
                self.points[game.team_a]["draws"] += 1
                self.points[game.team_b]["points"] += 1
                self.points[game.team_b]["draws"] += 1
                self.points[game.team_a]["goals_for"] += game.score[game.team_a.name]
                self.points[game.team_a]["goals_against"] += game.score[game.team_b.name]
                self.points[game.team_b]["goals_for"] += game.score[game.team_b.name]
                self.points[game.team_b]["goals_against"] += game.score[game.team_a.name]
                self.points[game.team_a]["goal_difference"] += game.score[game.team_a.name] - game.score[game.team_b.name]
                self.points[game.team_b]["goal_difference"] += game.score[game.team_b.name] - game.score[game.team_a.name]
    def display_standings(self):
        """ Display the standings of the group. """
        dsort = sorted(self.points.items(), key=lambda x: x[1]["points"], reverse=True) #sort by points
        print(f"Group: {self.name}")
        print(f"{'Team':<20} {'Pts':<2} {'W':<2} {'L':<2} {'D':<2} {'GF':<2} {'GA':<2} {'GD':<2}")
        for team, stats in dsort:
            print(f"{str(team.name):<20} {stats['points']:2} {stats['wins']:2} {stats['losses']:2} {stats['draws']:2}  {stats['goals_for']} :{stats['goals_against']:2} {stats['goal_difference']:2}")
    def get_qualified_teams(self):
        """ Get the qualified teams for the next stage. """
        dsort = sorted(self.points.items(), key=lambda x: x[1]["points"], reverse=True) #sort by points
        return [team for team, stats in dsort[2:]]