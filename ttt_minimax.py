#!/bin/env python3

from TicTacToe import TicTacToe
from random import choice as random_choice
from time import time
import logging


def create_console_logger(level: str, format: str) -> logging.Logger:
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, level))

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level))

    # Create formatter
    formatter = logging.Formatter(format)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


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


def minimax(board, depth, is_maximizing_player):
    global move_inspections
    move_inspections += 1
    #print("Entering minimax()..")
    #print("Maximizing player: {}".format(is_maximizing_player))
    """
    Return when a leaf node is found:
        * board.is_tie() : 0
        * board.winner() == 'X' : 1
        * board.winner() == 'O' : -1
    """
    if board.winner() == 'X':
        value = 1
        log.debug(f"X wins this path!: Returning {value}")
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
            score = minimax(board, depth-1, not is_maximizing_player)
            tmpScore = min(score, bestScore)
            if tmpScore < bestScore:
                bestScore = tmpScore
            board.undo_last_move()
    else:  # minimizing player
        # What would the maximizing player pick next?
        bestScore = -2
        for move in moves:
            log.debug(f"Trying {move} for the maxi player")
            board.update_board(move)
            score = minimax(board, depth-1, not is_maximizing_player)
            tmpScore = max(score, bestScore)
            if tmpScore > bestScore:
                bestScore = tmpScore
            board.undo_last_move()
    log.debug(f"Returning {bestScore} up the chain")
    return bestScore


def best_move(board, is_maxi_player):
    print("Entering best_move()")
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
        # Run board through minimax()
        score = minimax(board, len(moves), is_maxi_player)

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
    """
    There should only be 255168 inspections for the 1st move
    """
    # Global vars
    global log, move_inspections

    # Vars
    game_over = False
    maxi_player = True

    # Set up a logger
    log = create_console_logger('DEBUG', '%(levelname)s: %(message)s')

    t0 = time()
    board = TicTacToe()
    t1 = time()
    print("It took {} usecs to initialize my board".format(t1-t0))

    # Create a starting board
    starting_board = [1, 5, 3, 2, 8, 4]
    #starting_board = [1, 5, 9]
    #starting_board = []
    #starting_board = []
    setup_board(board, starting_board)

    """
    Starting board
     X | O | X
    -----------
     O | O |
    -----------
       | X |

    """
    board.draw()
    while not game_over:
        if maxi_player:  # computer player
            # Reset inspection count
            move_inspections = 0
            board.update_board(best_move(board, maxi_player))
            print(f"{move_inspections} moves were inspected")
        else:
            board.update_board(get_player_move(board))
        board.draw()
        maxi_player = not maxi_player
        # end or switch players
        game_over = board.winner() or board.is_tie()

    if board.winner():
        print(f"{board.winner()} is the winner!")
    else:
        print("Tie game!")


if __name__ == "__main__":
    main()
