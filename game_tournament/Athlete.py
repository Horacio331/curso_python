class Athlete:
    """ Athlete class representing a player  in the tournament. """
    def __init__(self, name):
        """Custom constructor fot Athlete class."""
        self.name = name
        self.number=0
    def __str__(self):
        """ String representation of the Athlete object."""
        return f"Athlete: {self.name}, Number: {self.number}"
    def __repr__(self):
        """Official String representation of the Athlete object. """
        return f"Athlete(name='{self.name}', number={self.number})"

if __name__ == "__main__":
    #Example usage
    athlete1 = Athlete("Lionel Messi")
    athlete1.number = 10
    print(athlete1) #Output: Athlete: Lionel Messi, number: 10
    print(repr(athlete1)) #Output: Athlete (name='Lionel Messi', number=10)