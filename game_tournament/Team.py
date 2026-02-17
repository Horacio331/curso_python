"""
Docstring for game_tournament.Team
"""
from Athlete import Athlete
from Sport import Sport

class Team:
    """ Team class represents a team in the tournament. It has a name, a sport, and a list of athletes. """
    def __init__(self, name, sport:Sport):
        """ Custom constructor for Team class. """
        self.name = name
        self.set_sport(sport)
        self.athletes = []
    def set_sport(self, sport):
        """ Set the sport for the team. """
        if isinstance(sport, Sport):
            self.sport = sport
        else:
            raise ValueError("Only Sport objects can be set as the team's sport.")
    def add_athlete(self, athlete):
        """ Add an athlete to the team. """
        if isinstance(athlete, Athlete):
            self.athletes.append(athlete)
        else:
            raise ValueError("Only Athlete objects can be added to the team.")
    def __str__(self):
        """ String representation of the Team class. """
        return f"{self.name} - {self.sport.name} ({len(self.athletes)} athletes)"
    def __repr__(self):
        """ String representation of the Team class. """
        return f"Team(name={self.name}, sport={repr(self.sport)})"
    def to_json(self):
        """ Convert the Team object to a JSON string. """
        return {
            "name": self.name,
            "sport": self.sport.to_json(),
            "athletes": [athlete.to_json() for athlete in self.athletes]
        }

if __name__ == "__main__":
    a = Athlete("Lionel Messi")
    b = Athlete("Diego Armando")
    s = Sport("Futbol",11,"FIFA")
    argentina  = Team("Argentina",s)
    argentina.add_athlete(a)
    argentina.add_athlete(b)
    print(argentina)
    print(repr(argentina))
    print(argentina.to_json())