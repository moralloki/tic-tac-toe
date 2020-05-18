class TicTacToe:
    markers = ['X', 'O']

    def __init__(self, markers=markers, empty_marker=" "):
        self.empty_marker = empty_marker
        self.board = [[self.empty_marker for _ in range(3)] for _ in range(3)]
        self.available_locations = [_ for _ in range(1, 10)]
        self.turn_number = 0
        self.markers = markers

    def __repr__(self):
        return "TicTacToe()"

    def __increment_turn(self):
        self.turn_number += 1

    def __map_num_to_tuple(self, selection: int) -> tuple:
        """
        1 2 3     0|0, 0|1, 0|2
        4 5 6 --> 1|0, 1|1, 1|2
        7 8 9     2|0, 2|1, 2|2
        """
        selection -= 1
        return (selection // 3, selection % 3)

    def get_available_locations(self):
        return self.available_locations

    def draw(self):
        for i in range(3):
            print("\t {} | {} | {}".format(
                self.board[i][0],
                self.board[i][1],
                self.board[i][2])
            )
            if i != 2:
                print("\t-----------")

    def get_turn(self):
        return self.turn_number

    def is_draw(self):
        for row in self.board:
            if self.empty_marker in row:
                return False
        return True

    def space_is_free(self, location):
        return location in self.available_locations

    def update_board(self, location):
        # Turn this into a method
        marker = self.markers[self.get_turn() % len(self.markers)]
        if self.space_is_free(location):
            i, j = self.__map_num_to_tuple(location)
            self.board[i][j] = marker
            self.__increment_turn()
            self.available_locations.remove(location)
        else:
            raise ValueError

    def winner(self):
        winner = None
        for i in range(3):
            # Horizontal
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != self.empty_marker:
                winner = self.board[i][0]
            # Vertical
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != self.empty_marker:
                winner = self.board[0][i]
            # Diagonal
            if self.board[1][1] != self.empty_marker:
                if self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[2][0] == self.board[1][1] == self.board[0][2]:
                    winner = self.board[1][1]
        return winner
