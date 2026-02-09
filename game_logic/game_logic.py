"""
Docstring for game_logic
Author: Duran Salido Horacio
Here goes the game logic for Tictactoe
"""
import board

def check_winner(d:dict, combo_list:list)->bool:
    """
    Check if there is a winner
    """
    for combo in combo_list:
        if d[combo[0]] == d[combo[1]] == d[combo[2]]:
            return True
    return False

def game():
    """
    Here lives the main game loop
    """
    turns = 0
    dboard = {x:str(x) for x in range(9)}
    combo_list = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # columns
        [0,4,8], [2,4,6]           # diagonals
    ]
    x_player = 'X'
    o_player = 'O'
    current_player = x_player
    winner = False
    w_player = ""
    while turns < 9 and not winner:
        board.display_board(dboard)
        valid_move = False
        while not valid_move:
            valid_move = board.player_turn(current_player, dboard)
        turns += 1
        winner = check_winner(dboard, combo_list)
        if winner:
            w_player = current_player
        if current_player == x_player:
            current_player = o_player
        else:
            current_player = x_player
    board.display_board(dboard)
    if winner:
        print(f"Winner: Player {w_player}")
    else:
        print(f"It's a tie!")
if __name__ == "__main__":
    game()