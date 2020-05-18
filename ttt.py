#!/bin/env python3


from TicTacToe import TicTacToe
from copy import deepcopy
from random import choice as random_choice


def computer_move(board):
    center = [5]
    corners = [1, 3, 7, 9]
    edges = [2, 4, 6, 8]
    available_moves = board.get_available_locations()
    print("Computer is choosing from: {}".format(available_moves))

    # Can I win on my next move?
    for move in available_moves:
        # Create a board copy
        board_copy = deepcopy(board)
        board_copy.update_board(move)
        if board_copy.winner():
            return move

    # Can I block against a win with my next move?
    for move in available_moves:
        # Create a board copy
        board_copy = deepcopy(board)
        # Switch to the next player
        board_copy.turn_number += 1
        board_copy.update_board(move)
        if board_copy.winner():
            return move

    # Run through corners, center, then edges for next available move
    for l in corners, center, edges:
        choices = list(set(l).intersection(available_moves))
        if choices:
            choice = random_choice(choices)
            break
    # BUG: This doesn't always print
    print("Computer choose {}. Your move...".format(choice))
    return choice


def get_player_move(board) -> int:
    """Get user input for next square to select

    Raises:
        ValueError: When input is not between 1 through 9 (inclusive)

    Returns:
        int -- 1-9
    """
    selection = int(
        input("Select an unoccupied square {}: ".format(board.get_available_locations())))

    if not 1 <= int(selection) <= 9:
        raise ValueError
    return selection


def main():
    # Global vars
    game_over = False
    is_human_turn = True

    # Start with Human player as 'X' (default)
    board = TicTacToe()
    while not game_over:
        board.draw()
        if is_human_turn:
            try:
                selection = get_player_move(board)
                board.update_board(selection)
            except ValueError:
                print("Sorry, please select an unoccupied square {}".format(
                    board.available_locations))
                continue
        else:
            board.update_board(computer_move(board))
        if board.winner():
            print(f"{board.winner()} is the winner!")
            game_over = True
            continue
        if board.is_draw():
            print("It's a draw!")
            game_over = True
            continue
        # Flip our player
        is_human_turn = not is_human_turn

    board.draw()


if __name__ == "__main__":
    main()
