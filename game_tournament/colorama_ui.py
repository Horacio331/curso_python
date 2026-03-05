""" Text user interface for the tournament """
import os
import colorama
from Tournament import Tournament
from colorama import Fore, Back, Style, init
init(autoreset=False)

class ColoramaUI:
    def __init__(self):
        self.tournament = None
        self.current_file = None 
    def set_current_file(self, file_path: str):
        self.current_file = file_path
    def run (self):
        """ Run the colorama ui """
        colorama.init(autoreset=False)
        self.display_menu()
    def show_menu(self):
        """ Show the menu """
        while True:
            print("\nTournament")
            print("1. Load tournament")
            print("2. Display tournament")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                file_path = input("Engter the path to the JSON file: ")
                self.set_current_file(file_path)
                self.open_tournament(file_path)
            elif choice == "2":
                self.display_tournament()
            elif choice == "3":
                self.exit_app()
            else:
                print("Invalid choice. Please try again.")
    def open_tournament(self):
        """ Open tournament from JSON file """
        self.tournament = Tournament("Tournament")
        self.tournament.load_json(self.current_file)
        self.tournament.set_group_stage()
    def display_tournament(self):
        """ Display tournament """
        # Set colors before clearing screen to fill background
        print(Back.LIGHTBLACK_EX + Fore.WHITE, end="")
        os.system("cls" if os.name == "nt" else "clear")
        
        print(str(self.tournament))
        for group in self.tournament.groups:
            print(group)
        for game in self.tournament.games:
            print(game)
        
        # Reset and clear for menu
        print(Style.RESET_ALL, end="")
        os.system("cls" if os.name == "nt" else "clear")
    def exit_app(self):
        """ Exit the application """
        print("Exiting application...")
        exit()
    def get_tournament_json(self):
        """ Get the tournament """
        file_path = input("Enter the path to the JSON file: ")
        self.set_current_file(file_path)
        self.open_tournament()
    def display_menu(self):
        """ Show the menu """
        print(f"Current file: {self.current_file}")
        dictionary_menu = {
            "1": "Load tournament",
            "2": "Display tournament",
            "3":"Display groups",
            "4": "Display games",
            "5": "Play games",
            "6": "Exit"
        }
        action_dictionary = {
            "1": self.get_tournament_json,
            "2": self.display_tournament,
            "3": self.display_groups,
            #"4": self.display_games,
            #"5": self.play_games,
            "6": self.exit_app
        }
        while True:
            print("\nTournament")
            for key in sorted(dictionary_menu.keys()):
                print(f"{key}. {dictionary_menu[key]}")
            choice = input("Enter your choice: ")
            if choice in action_dictionary:
                action_dictionary[choice]()
            else:
                print("Invalid choice. Please try again.")
    def display_groups(self):
        """ Display groups """
        # Set colors before clearing screen to fill background
        print(Back.CYAN + Fore.WHITE, end="")
        os.system("cls" if os.name == "nt" else "clear")

        print(str(self.tournament))
        for group in self.tournament.groups.keys():
            print(Back.GREEN + Fore.WHITE, end="")
            self.tournament.groups[group].display_group()
            print(Style.RESET_ALL + Back.CYAN + Fore.WHITE, end="") # Preserve background
        
        print(Style.RESET_ALL, end="") # Final reset for the text block
        
        # Reset and clear for menu
        print(Style.RESET_ALL, end="")
        
if __name__ == "__main__":
    ui = ColoramaUI()
    ui.set_current_file("tournament.json")
    ui.open_tournament()
    ui.run()