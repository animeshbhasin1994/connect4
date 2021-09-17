import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):
    def test_reset_game(self):
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
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.make_p1_move(1, 2)
        self.assertEqual('red', game.board[1][2])
        self.assertEqual(game.current_turn, 'p2')
        self.assertEqual(game.remaining_moves, 41)

    def test_make_p2_move(self):
        game = Gameboard()
        game.set_player_color('p2', 'yellow')
        game.make_p2_move(1, 5)
        self.assertEqual('yellow', game.board[1][5])
        self.assertEqual(game.current_turn, 'p1')
        self.assertEqual(game.remaining_moves, 41)

    def test_four_in_a_row_check_vertical(self):
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
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 'yellow', 'yellow', 'yellow', 0, 0],
                      [0, 0, 'red', 'red', 'red', 'red', 0]]

        self.assertTrue(game.four_in_a_row_check('red'))

    def test_four_in_a_row_check_positive_diaganol(self):
        game = Gameboard()
        game.set_player_color('p1', 'red')
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 'red', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 'red', 'red', 'yellow', 0, 0, 'red'],
                      ['red', 'yellow', 'yellow', 'yellow', 0, 0, 'yellow']]

        self.assertTrue(game.four_in_a_row_check('red'))

    def test_four_in_a_row_check_negative_diaganol(self):
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
        game = Gameboard()
        game.remaining_moves = 0
        game.check_game_over('red')
        self.assertEqual('draw - no winner', game.game_result)

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
        game = Gameboard()
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(5, game.next_move_row_index(0))

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0]]

        self.assertEqual(4, game.next_move_row_index(0))

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0]]

        self.assertEqual(0, game.next_move_row_index(0))


if __name__ == '__main__':
    unittest.main()
