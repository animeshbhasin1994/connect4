import db
import ast


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

    def set_player_color(self, player, color):
        if player == 'p1':
            self.player1 = color
        else:
            self.player2 = color

    def next_move_row_index(self, col):
        for i in range(6):
            if self.board[i][col] != 0:
                return i - 1
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
                if self.board[i + 3][j] == color \
                        and self.board[i + 2][j] == color \
                        and self.board[i + 1][j] == color \
                        and self.board[i][j] == color:
                    return True

        for j in range(4):
            for i in range(6):
                if self.board[i][j + 3] == color \
                        and self.board[i][j + 2] == color \
                        and self.board[i][j + 1] == color \
                        and self.board[i][j] == color:
                    return True

        for j in range(4):
            for i in range(3):
                if self.board[i + 3][j + 3] == color \
                        and self.board[i + 2][j + 2] == color \
                        and self.board[i + 1][j + 1] == color \
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
        if self.remaining_moves <= 0:
            self.game_result = "draw - no winner"
        if self.four_in_a_row_check(color):
            self.game_result = 'p1' if color == self.player1 else 'p2'

    def get_error_move_reason(self, current_turn='p1'):
        if self.game_result:
            return 'Game is over'
        if current_turn == 'p1':
            if not self.player1:
                return 'Please select color first'
            if self.current_turn == 'p2':
                return 'Player 2 has to move, please wait'
        else:
            if not self.player2:
                return 'Please select color first'
            if self.current_turn == 'p1':
                return 'Player 1 has to move, please wait'

    def get_column_full_error(self, col_no):
        if self.board[0][col_no] != 0:
            return 'Column is full, please play in some other column'

        return False

    def set_base_config(self, game_state_tuple):
        self.current_turn = game_state_tuple[0]
        self.board = ast.literal_eval(game_state_tuple[1])
        self.game_result = game_state_tuple[2]
        self.player1 = game_state_tuple[3]
        self.player2 = game_state_tuple[4]
        self.remaining_moves = game_state_tuple[5]

    def set_game_config(self, player, status=None):
        game_state_tuple = db.getMove()
        if game_state_tuple:
            self.set_base_config(game_state_tuple)
        else:
            if player == 'p1':
                self.set_player_color('p1', status)
            else:
                if self.player1 == 'red':
                    self.set_player_color('p2', 'yellow')
                elif self.player1 == 'yellow':
                    self.set_player_color('p2', 'red')
                else:
                    self.set_player_color(
                        'p2', 'Please wait for p1 to select color')

    def get_game_config(self):
        return (self.current_turn, self.board, self.game_result,
                self.player1, self.player2, self.remaining_moves)
