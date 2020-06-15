"""
The classic tic-tac-toe game

Xs and Os battle it out in alternating moves attempting
to win by getting 3 marks in a horizontal, vertical
or diagonal row.

Notes:
    * X always starts
    * Games can end in a tie
"""


class TicTacToe:

    def __init__(self):
        self.empty_marker = " "
        self.board = [[self.empty_marker for _ in range(3)] for _ in range(3)]
        self.available_locations = [_ for _ in range(1, 10)]
        self._markers = ['X', 'O']
        self._move_stack = []
        self.init_end_state()

    def init_end_state(self):
        self._end_state = {
            'is_tie': False,
            'winner': None,  # None, X, O
            'winning_type': None,  # 'column', 'diagonal', 'row'
            'winning_index': None,  # 0, 1, 2
            'winning_column': None,  # 0, 1, 2
            'winning_row': None,  # 0, 1, 2
            'winning_diagonal': None,  # 0 - ('\'), 1 - ('/')
        }

    def __repr__(self):
        tmpStr = ""
        for i in range(3):
            tmpStr += "\t {} | {} | {}\n".format(
                self.board[i][0],
                self.board[i][1],
                self.board[i][2])
            if i != 2:
                tmpStr += "\t-----------\n"
        # return "TicTacToe()"
        tmpStr = f"\t {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}\n"
        tmpStr += "\t-----------\n"
        tmpStr += f"\t {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}\n"
        tmpStr += "\t-----------\n"
        tmpStr += f"\t {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}"
        return tmpStr

    def __map_num_to_tuple(self, selection: int) -> tuple:
        """
        1 2 3     0|0, 0|1, 0|2
        4 5 6 --> 1|0, 1|1, 1|2
        7 8 9     2|0, 2|1, 2|2
        """
        selection -= 1
        return (selection // 3, selection % 3)

    def current_player(self):
        return self._markers[self.get_turn() % len(self._markers)]

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
        return len(self._move_stack)

    def is_tie(self):
        for row in self.board:
            if self.empty_marker in row:
                self._end_state['is_tie'] = True
                return False
        return True

    def is_win(self):
        return self._end_state['winner'] is not None

    def winner(self):
        return self._end_state['winner']

    def win_info(self):
        wtype = self._end_state['winning_type']
        index = self._end_state['winning_index']
        return {'type': wtype, 'index': index}

    def space_is_free(self, location):
        return location in self.available_locations

    def undo_last_move(self):
        """
        Pop last turn from the stack
            * return some error if stack is empty
        Update board with "empty" space
        Add spot back to available_locations
        Reset end state
        """
        if len(self._move_stack):
            last_move = self._move_stack.pop()
            i, j = self.__map_num_to_tuple(last_move)
            self.board[i][j] = self.empty_marker
            self.available_locations.append(last_move)
            self.available_locations.sort()
            self.init_end_state()
        else:
            print("No moves to undo...")

    def update_board(self, location):
        if self.space_is_free(location):
            i, j = self.__map_num_to_tuple(location)
            self.board[i][j] = self.current_player()
            self._move_stack.append(location)
            self.available_locations.remove(location)
            self.evaluate_baord()
        else:
            raise ValueError

    def evaluate_baord(self):
        winner = None
        for i in range(3):
            # Horizontal
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != self.empty_marker:
                winner = self.board[i][0]
                self._end_state['winning_row'] = i
                self._end_state['winning_index'] = i
                self._end_state['winning_type'] = 'row'
                break
            # Vertical
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != self.empty_marker:
                winner = self.board[0][i]
                self._end_state['winning_column'] = i
                self._end_state['winning_index'] = i
                self._end_state['winning_type'] = 'column'
                break
        # Diagonal
        if self.board[1][1] != self.empty_marker:
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                winner = self.board[1][1]
                self._end_state['winning_diagonal'] = 0
                self._end_state['winning_index'] = 0
                self._end_state['winning_type'] = 'diagonal'
            elif self.board[2][0] == self.board[1][1] == self.board[0][2]:
                winner = self.board[1][1]
                self._end_state['winning_diagonal'] = 1
                self._end_state['winning_index'] = 1
                self._end_state['winning_type'] = 'diagonal'
        if winner:
            self._end_state['winner'] = winner
