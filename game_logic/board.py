"""
Docstring for tictactoe. game_logic.board
Author: Duran Salido Horacio
"""

def display_board(dboard:dict)->None:
    """ Display game board of Tictactoe
    """
    d = dboard
    print(f"{d[0]:2s}|{d[1]:2s}|{d[2]:2s}")
    print("--+--+--")
    print(f"{d[3]:2s}|{d[4]:2s}|{d[5]:2s}")
    print("--+--+--")
    print(f"{d[6]:2s}|{d[7]:2s}|{d[8]:2s}")

def player_turn(player:str, dboard:dict)->bool:
    """ Ask player for their turn
    """
    valid_move = False 
    user_input = input(f"Player {player}, enter your move (0-8): ")
    user_input = int(user_input)
    print(f"Value entered: {user_input} type: {type(user_input)}")
    if user_input in dboard.keys():
        if dboard[user_input] not in ['X', 'O']:
            dboard[user_input] = player
            valid_move = True
        else:
            print("Invalid move: Cell already occupied.")
    else:
        print("Invalid move: Cell does not exist.")
    return valid_move

if __name__ == "__main__":
    board = {x:str(x) for x in range(9)}
    display_board(board)
    move = player_turn('X', board)
    print(f"Move valid: {move}")
    display_board(board)
    
    move = player_turn('O', board)
    print(f"Move valid: {move}")
    display_board(board)
    print(board)
    #board[0] = 'X'
    #board[4] = 'O'
    #display_board(board)