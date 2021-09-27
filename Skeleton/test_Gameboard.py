import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):
    def test_reset_game(self):
        # Checks if the game is correctly reset on restarting ( "/" endpoint)
        expected_game = Gameboard()
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.set_player_color('p2', 'yellow')
        game.make_p1_move(1, 2)
        game.make_p2_move(2, 2)
        game.make_p1_move(3, 2)
        game.reset_game()
        self.assertEqual(expected_game.board, game.board)
        self.assertEqual(expected_game.player1, game.player1)
        self.assertEqual(expected_game.player2, game.player2)
        self.assertEqual(expected_game.game_result, game.game_result)
        self.assertEqual(expected_game.current_turn, game.current_turn)
        self.assertEqual(expected_game.remaining_moves, game.remaining_moves)

    def test_set_player_color(self):
        # Checks if the colors are correctly assigned to each player
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.set_player_color('p2', 'yellow')
        self.assertEqual('red', game.player1)
        self.assertEqual('yellow', game.player2)

        game.set_player_color('p1', 'yellow')
        game.set_player_color('p2', 'red')
        self.assertEqual('yellow', game.player1)
        self.assertEqual('red', game.player2)

    def test_make_p1_move(self):
        #Happy path for correct move for p1
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.make_p1_move(1, 2)
        self.assertEqual('red', game.board[1][2])
        self.assertEqual(game.current_turn, 'p2')
        self.assertEqual(game.remaining_moves, 41)

    def test_make_p2_move(self):
        # Happy path for correct move for p2
        game = Gameboard()
        game.set_player_color('p2', 'yellow')
        game.make_p2_move(1, 5)
        self.assertEqual('yellow', game.board[1][5])
        self.assertEqual(game.current_turn, 'p1')
        self.assertEqual(game.remaining_moves, 41)

    def test_four_in_a_row_check_vertical(self):
        # Checks if there is a winning move in vertical direction
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'red', 0, 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0]]

        self.assertTrue(game.four_in_a_row_check('red'))

    def test_four_in_a_row_check_horizontal(self):
        # Checks if there is a winning move in horizontal direction
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'yellow', 'yellow', 'yellow', 0, 0],
                      [0, 0, 'red', 'red', 'red', 'red', 0]]

        self.assertTrue(game.four_in_a_row_check('red'))

    def test_four_in_a_row_check_positive_diagonal(self):
        # Checks if there is a winning move in positive diagonal direction
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 'red', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 'red', 'red', 'yellow', 0, 0, 'red'],
                      ['red', 'yellow', 'yellow', 'yellow', 0, 0, 'yellow']]

        self.assertTrue(game.four_in_a_row_check('red'))

    def test_four_in_a_row_check_negative_diagonal(self):
        # Checks if there is a winning move in negative diagonal direction
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 'red', 0, 0, 0, 0, 'red'],
                      ['yellow', 'yellow', 'red', 0, 0, 0, 'red'],
                      ['yellow', 'yellow', 'yellow', 'red', 0, 0, 'red']]

        self.assertTrue(game.four_in_a_row_check('red'))

    def test_four_in_a_row_check_draw(self):
        # Checks if there is a draw because board is filled and there is no 4 in a row
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = \
            [['yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'yellow'],
             ['yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'yellow'],
             ['yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'yellow'],
             ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red'],
             ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red'],
             ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red']]

        self.assertFalse(game.four_in_a_row_check('red'))




    def test_check_game_over(self):
        #Checks if the game_result variable is correctly assigned on game getting over

        #Checks if game.result = draw - no winner when remaining moves are 0 are game is draw
        game = Gameboard()
        game.remaining_moves = 0
        game.check_game_over('red')
        self.assertEqual('draw - no winner', game.game_result)

        #Checks if game.result = 'p1' if p1 gets 4 in a row
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'red', 0, 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0]]
        game.check_game_over('red')
        self.assertEqual('p1', game.game_result)

        # Checks if game.result = 'p2' if p2 gets 4 in a row
        game = Gameboard()
        game.set_player_color('p2', 'yellow')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 'yellow', 0, 0, 0, 0, 0],
                      [0, 'yellow', 'red', 0, 0, 0, 0],
                      [0, 'yellow', 'red', 0, 0, 0, 0],
                      [0, 'yellow', 'red', 0, 0, 0, 0]]
        game.check_game_over('yellow')
        self.assertEqual('p2', game.game_result)

    def test_next_move_row_index(self):
        #Check if the correct next position(row to insert) is picked for the tile to be placed
        game = Gameboard()
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

        #For column 0, since row 5 is empty, next move row index = 5
        self.assertEqual(5, game.next_move_row_index(0))

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0]]

        # For column 0, since row 4 is empty & row 5 is full, next move row index = 4
        self.assertEqual(4, game.next_move_row_index(0))

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0]]

        # For column 0, since row 1-5 is full, next move row index = 0
        self.assertEqual(0, game.next_move_row_index(0))

    def test_get_error_move_reason(self):
        # Invalid move - winner already declared
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'red', 0, 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0]]
        game.check_game_over('red')
        invalid_move_reason = game.get_error_move_reason(current_turn='p2')

        self.assertEqual('Game is over', invalid_move_reason)

        #Invalid move - not player 1's turn
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0]]
        game.make_p1_move(3, 2)
        invalid_move_reason = game.get_error_move_reason(current_turn='p1')

        self.assertEqual('Player 2 has to move, please wait', invalid_move_reason)

        #Invalid move - not player 2's turn
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.set_player_color('p2', 'yellow')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'red', 0, 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0]]
        game.make_p2_move(4, 3)
        invalid_move_reason = game.get_error_move_reason(current_turn='p2')

        self.assertEqual('Player 1 has to move, please wait', invalid_move_reason)

        # Invalid move - Player 1 does not select color before making move
        game = Gameboard()

        game.make_p1_move(0, 0)
        invalid_move_reason = game.get_error_move_reason(current_turn='p1')

        self.assertEqual('Please select color first', invalid_move_reason)

        # Invalid move - Player 2 does not select color before making move
        game = Gameboard()

        game.make_p2_move(0, 0)
        invalid_move_reason = game.get_error_move_reason(current_turn='p2')

        self.assertEqual('Please select color first', invalid_move_reason)

    def test_get_column_full_error(self):
        # Invalid Move - Current column is filled

        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0]]
        game.make_p1_move(0, 0)
        invalid_move_reason = game.get_column_full_error(col_no=0)
        self.assertEqual('Column is full, please play in some other column', invalid_move_reason)

        # Valid Move - Current column is not filled

        game = Gameboard()
        game.set_player_color('p1', 'red')

        invalid_move_reason = game.get_column_full_error(col_no=0)
        self.assertFalse(invalid_move_reason)
if __name__ == '__main__':
    unittest.main()
