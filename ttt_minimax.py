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


def minimax(board, maximixingPlayer):
    if board.winner():
        if maximixingPlayer:
            value = 1
            print(f"WIN!: Returning {value}")
            board.draw()
            return 1
        else:
            value = -1
            print(f"LOSS!: Returning {value}")
            board.draw()
            return -1
    if board.is_draw():
        print("DRAW: Returning 0")
        board.draw()
        return 0
    # win/loss is unknown, go deeper
    print("No end in sight, going deeper...")
    if maximixingPlayer:
        bestScore = -2
        board_copy = deepcopy(board)
        next_moves = board_copy.get_available_locations()
        for move in next_moves:
            print(f"Trying {move} for the mini player")
            board_copy.update_board(move)
            # return min(value, minimax(board_copy, not maximixingPlayer))
            score = minimax(board_copy, not maximixingPlayer)
            bestScore = max(score, bestScore)
        print(f"Returning {bestScore} up the chain")
        return bestScore
    else:
        bestScore = 2
        board_copy = deepcopy(board)
        next_moves = board_copy.get_available_locations()
        for move in next_moves:
            print(f"Trying {move} for the maxi player")
            board_copy.update_board(move)
            #score = max(value, minimax(board_copy, not maximixingPlayer))
            score = minimax(board_copy, not maximixingPlayer)
            bestScore = min(score, bestScore)
        print(f"Returning {bestScore} up the chain")
        return bestScore


def best_move(board):
    bestScore = -2
    bestMove = None
    print(f"Current best score: {bestScore}")
    print("Current best move: Unknown")
    for move in board.get_available_locations():
        print(f"Trying out {move}")
        board_copy = deepcopy(board)
        board_copy.update_board(move)
        score = minimax(board_copy, True)
        if score > bestScore:
            print(f"That's a better result ({move})! Updating...")
            bestScore = score
            bestMove = move
    return bestMove


def main():
    # Global vars
    game_over = False

    board = TicTacToe()
    """
    Starting board
     X | O | O
    -----------
       | O | X
    -----------
       | X | X
    """
    board.update_board(1)
    board.update_board(5)
    board.update_board(8)
    board.update_board(2)
    board.update_board(9)
    board.update_board(3)
    while not game_over:
        board.draw()
        print()
        board.update_board(best_move(board))
        print()
        board.draw()
        exit(0)
        if board.winner():
            print(f"{board.winner()} is the winner!")
            game_over = True
            continue
        if board.is_draw():
            print("It's a draw!")
            game_over = True
            continue

    board.draw()


if __name__ == "__main__":
    main()
