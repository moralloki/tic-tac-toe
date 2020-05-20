#!/bin/env python3

from TicTacToe import TicTacToe
from copy import deepcopy
from logging import getLogger
from random import choice as random_choice

# Set up a logger
log = getLogger(__name__)


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


def minimax(board, is_maximizing_player):
    """
    Return when a leaf node is found:
        * board.is_tie() : 0
        * board.winner() == 'X' : 1
        * board.winner() == 'O' : -1
    """
    if board.winner() == 'X':
        value = 1
        log.debug(f"X wins this path!: Returning {value}")
        # board.draw()
        return value
    elif board.winner() == 'O':
        value = -1
        log.debug(f"O wins this path!: Returning {value}")
        # board.draw()
        return value
    elif board.is_tie():
        value = 0
        log.debug(f"It's a tie: Returning {value}")
        # board.draw()
        return value
    # win/loss is unknown, go deeper
    log.debug("No end in sight, going deeper...")
    moves = board.available_locations[:]  # another copy!
    if is_maximizing_player:
        # What would the minimizing player pick next?
        bestScore = 2
        for move in moves:
            log.debug(f"Trying {move} for the mini player")
            board.update_board(move)
            score = minimax(board, not is_maximizing_player)
            tmpScore = min(score, bestScore)
            if tmpScore < bestScore:
                bestScore = tmpScore
            board.undo_last_move()
        log.debug(f"Returning {bestScore} up the chain")
        return bestScore
    else:  # minimizing player
        # What would the maximizing player pick next?
        bestScore = -2
        for move in moves:
            log.debug(f"Trying {move} for the maxi player")
            board.update_board(move)
            score = minimax(board, not is_maximizing_player)
            tmpScore = max(score, bestScore)
            if tmpScore > bestScore:
                bestScore = tmpScore
            board.undo_last_move()
        log.debug(f"Returning {bestScore} up the chain")
        return bestScore


def best_move(board, is_maxi_player):
    if is_maxi_player:
        bestScore = -2
        marker = 'X'
    else:
        bestScore = 2
        marker = 'O'
    bestMove = None
    log.debug(f"Looking for {marker}'s best move...'")
    log.debug(f"Current best score: {bestScore}")
    log.debug(f"Current best move: {bestMove}")

    # Run through all of the possible moves
    moves = board.available_locations[:]  # need to make a copy
    log.debug(f"Possible moves: {moves}")

    for move in moves:
        log.debug(f"Trying out {move}")
        board.update_board(move)
        # Run suggested board through minimax()
        score = minimax(board, is_maxi_player)

        log.debug(f"Checking if {score} is better than {bestScore}...")
        if is_maxi_player:
            if score > bestScore:
                log.debug(
                    f"That's a higher score! So far {move} is the best choice...")
                bestScore = score
                bestMove = move
        else:
            if score < bestScore:
                log.debug(
                    f"That's a lower score! So far {move} is the best choice...")
                bestScore = score
                bestMove = move
        board.undo_last_move()
    print(f"Computer selected {bestMove} as it's move...")
    return bestMove


def setup_board(board, move_list):
    for move in move_list:
        board.update_board(move)


def main():
    # Global vars
    game_over = False
    maxi_player = False

    board = TicTacToe()

    # Create a starting board
    #starting_board = [1, 5, 9, 2, 8, 3]
    #starting_board = [1, 5, 9]
    starting_board = []
    setup_board(board, starting_board)

    """
    Starting board
     X | O | O
    -----------
       | O |
    -----------
       | X | X

    X is next move
    Should iterate through as:

    X    O    X
    ------------
    4-> 6-> 7 == X wins (+1)
    4-> 7     == O wins (-1)
    # Since O can win, move 4 == -1 score
    6-> 4-> 7 == X wins (+1)
    6-> 7     == O wins (-1) no final move to check
    # Since O can win, move 6 == -1 score
    7         == X wins (+1)
    # Only 1 outcome, move 7 == +1 score
    """
    board.draw()
    while not game_over:
        if maxi_player:
            board.update_board(best_move(board, maxi_player))
        else:
            board.update_board(get_player_move(board))
        board.draw()
        # end or switch players
        if board.winner() or board.is_tie():
            game_over = True
        else:
            maxi_player = not maxi_player

    if board.winner():
        print(f"{board.winner()} is the winner!")
    else:
        print("Tie game!")


if __name__ == "__main__":
    main()
