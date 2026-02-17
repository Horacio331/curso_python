""" 
| Athlete class representing a player in the tournament. | """
import random

class  Athlete:
    """ Athlete class representing a player in the tournament. """
    def __init__(self, name):
        """ Custom constructor for Athlete class. """
        self.name = name
        self.number= random.randint(1, 99)  # Assign a random number to the athlete
    def __str__(self):
        """ String representation of the Athlete object. """
        return f"Athlete: {self.name}, Number: {self.number}"
    def __repr__(self):
        """ Official string representation of the Athlete object. """
        return f"Athlete(name='{self.name}', number={self.number})"
    def set_number(self, number):
        """ Set the athlete's number. """
        self.number = number
    def to_json(self):
        """ Generate json of Athlete"""
        return {
                "name":self.name, 
                "number":self.number
                }

if  __name__ == "__main__":
    # Example usage
    athlete1 = Athlete("Lionel Messi")
    athlete1.set_number(10)
    print(athlete1)  # Output: Athlete: Lionel Messi, Number: 10
    print(repr(athlete1))  # Output: Athlete(name='Lionel Messi', number=10)