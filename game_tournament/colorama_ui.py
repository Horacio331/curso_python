"""Tex"""
from colorama import Fore, Back, Style, init
init(autoreset=True)

class ColoramaUI:
    def __init__(self):
        self.tournament = None
        self.current_file = None
    def set_current_file(self, file_path: str):
        self.current_file = file_path
    def run (self):
        """ Main loop of the UI.   """
        colorama.init(autoreset=True)
        self.show_menu()
    def show_menu(self):
        """ Show the main menu of the UI. """
        while True:
            print