""" Text user interface for the tournament """
import os
import colorama
from Tournament import Tournament
from colorama import Fore, Back, Style, init
init(autoreset=True)

class ColoramaUI:
    def __init__(self):
        self.tournament = None
        self.current_file = None 
    def set_current_file(self, file_path: str):
        self.current_file = file_path
    def run (self):
        """ Run the colorama ui """
        colorama.init(autoreset=True)
        self.show_menu()
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
    def open_tournament(self, file_path: str):
        """ Open tournament from JSON file """
        self.tournament = Tournament("Tournament")
        self.tournament.load_json(file_path)
    def display_tournament(self):
        """ Display tournament """
        # clear screen
        os.system("cls" if os.name == "nt" else "clear")
        # set background color to gray and text colo to white
        print(Back.LIGHTBLACK_EX + Fore.WHITE + str(self.tournament))
        for group in self.tournament.groups:
            print(group)
        for game in self.tournament.games:
            print(game)
        else: 
            print("No tournament loaded.")
    def exit_app(self):
        """ Exit the application """
        print("Exiting application...")
        exit()

if __name__ == "__main__":
    ui = ColoramaUI()
    ui.run()