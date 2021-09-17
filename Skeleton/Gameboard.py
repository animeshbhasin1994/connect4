# import db


class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    '''
    Add Helper functions as needed to handle moves and update board and turns
    '''
    def reset_game(self):
        self.__init__()

    def next_move_row_index(self, col):
        for i in range(6):
            if self.board[i][col] != 0:
                return i-1
        return 5

    def make_p1_move(self, row_idx, col_no):
        self.board[row_idx][col_no] = self.player1
        self.current_turn = 'p2'
        self.remaining_moves -= 1

    def make_p2_move(self, row_idx, col_no):
        self.board[row_idx][col_no] = self.player2
        self.current_turn = 'p1'
        self.remaining_moves -= 1

    def four_in_a_row_check(self, color):
        for j in range(7):
            for i in range(3):
                if self.board[i+3][j] == color \
                        and self.board[i + 2][j] == color \
                        and self.board[i + 1][j] == color \
                        and self.board[i][j] == color:
                    return True

        for j in range(4):
            for i in range(6):
                if self.board[i][j+3] == color \
                        and self.board[j][j + 2] == color \
                        and self.board[i][j + 1] == color \
                        and self.board[i][j] == color:
                    return True

        for j in range(4):
            for i in range(3):
                if self.board[i + 3][j + 3] == color  \
                        and self.board[i + 2][j + 2] == color \
                        and self.board[i + 1][j + 1] == color\
                        and self.board[i][j] == color:
                    return True

        for j in range(4):
            for i in range(3, 6):
                if self.board[i - 3][j + 3] == color \
                        and self.board[i - 2][j + 2] == color \
                        and self.board[i - 1][j + 1] == color \
                        and self.board[i][j] == color:
                    return True

    def check_game_over(self, color):
        if self.remaining_moves == 0:
            self.game_result = ""
        if self.four_in_a_row_check(color):
            self.game_result = 'p1' if color == self.player1 else 'p2'
