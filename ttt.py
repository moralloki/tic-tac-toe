#!/bin/env python3


from TicTacToe import TicTacToe


def select_square_or_quit() -> int:
    """Get user input for next square to select

    Raises:
        ValueError: When input is not between 1 through 9 (inclusive)
        SystemExit: Raised when 'Q' or 'q' is input

    Returns:
        int -- 1-9
    """
    selection = input("Select an unoccupied square (1-9, or 'q' to quit): ")

    if selection.lower() == 'q':
        raise SystemExit
    if not 1 <= int(selection) <= 9:
        raise ValueError
    return int(selection)


def main():
    # Global vars
    game_over = False
    markers = ['A', 'B']

    board = TicTacToe(markers)
    while not game_over:
        board.draw()
        try:
            selection = select_square_or_quit()
            board.update_board(selection)
            # selection, markers[board.get_turn() % len(markers)])
        except ValueError:
            print("Sorry, please select an unoccupied square (1-9)")
            continue
        except SystemExit:
            print("Thanks for playing...")
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
