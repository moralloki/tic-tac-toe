#!/bin/env python3


def print_board_row(board: list) -> None:
    """Helper function to print out our tic-tac-toe board

    Arguments:
        board {list} -- A list of 3 3-element lists consisting of 'X', 'O', or '_'

    Returns:
        None
    """
    for row in board:
        # print("|".join(row))
        # print("-"*5)
        print(row)


def print_board_list(board: list) -> None:
    """Helper function to print out our tic-tac-toe board (using list comprehension)

    Arguments:
        board {list} -- A list of 3 3-element lists consisting of 'X', 'O', or '_'

    Returns:
        None
    """
    [print(row) for row in board]


def board_init() -> list:
    """Generate our tic-tac-toe board

    Returns:
        list -- A list of 3 3-element lists containing only '_'
    """

    # Potential alternate implementation
    # board = [ None, None, "O", "X", "O", None, "O", None, "X"]

    # Statically
    """
    board = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
    ]
    """
    # With list comprehension!
    return [["_" for _ in range(3)] for _ in range(3)]


def select_square() -> int:
    """Get user input for next square to select

    Raises:
        ValueError: Raised when any non-valid input is entered

    Returns:
        int -- 1-9
    """
    selection = int(input("Select an unoccupied square (1-9): "))

    if not 1 <= selection <= 9:
        raise ValueError
    return int(selection)


def convert_selection(selection: int) -> tuple:
    """[summary]

    Arguments:
        selection {int} -- 1-9

    Returns:
        tuple -- Converted (row, column) indicies
    """

    """
    1 2 3     0|0, 0|1, 0|2
    4 5 6 --> 1|0, 1|1, 1|2
    7 8 9     2|0, 2|1, 2|2
    """
    selection -= 1
    return (selection // 3, selection % 3)
    #row = floor((selection-1) / 3)
    #column = (selection-1) % 3


def update_board(board: list, selection: tuple, marker: chr = 'X') -> None:
    i, j = selection
    if board[i][j] == '_':
        board[i][j] = marker
    else:
        raise ValueError


def is_draw(board: list) -> bool:
    for row in board:
        if '_' in row:
            return False
    print("Draw! No more moves...")
    return True


def is_win(board: list) -> bool:
    """[summary]

    Arguments:
        board {list} -- [description]

    Returns:
        bool -- [description]
    """

    """
    1 - All values in a row match
    2 - All values in a column match
    3 - All values on a diagonal match
    """
    for i in range(3):
        # Horizontal
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '_':
            print(f"{board[i][0]} is the Winner with 3 in a row!")
            return True
        # Vertical
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '_':
            print(f"{board[i][0]} is the Winner with 3 in a column!")
            return True
        # Diagonal
        if board[1][1] != '_':
            if board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[1][1] == board[0][2]:
                print(f"{board[1][1]} is the Winner with 3 on the diagonal!")
                return True
    return False


def main():
    # Global vars
    game_over = False
    markers = ['X', 'O']
    turn = 0

    # Initialize our board
    board = board_init()
    while not game_over:
        print_board_row(board)
        try:
            selection = select_square()
            coordinates = convert_selection(selection)
            update_board(board, coordinates, markers[turn % 2])
        except ValueError:
            print("Sorry, please select an unoccupied square (1-9)")
            continue
        turn += 1
        game_over = is_draw(board) or is_win(board)

    print_board_row(board)


if __name__ == "__main__":
    main()
