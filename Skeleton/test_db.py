import unittest
import db
import sqlite3
import sys
import io


class Test_TestDb(unittest.TestCase):
    def test_init_db(self):
        # Happy Path - Check if new table called GAME is created successfully
        db.clear()
        db.init_db()
        conn = sqlite3.connect('sqlite_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name FROM sqlite_master WHERE type=\'table\' AND '
            'name=\'GAME\';')

        rows = cursor.fetchone()
        table_name = rows[0]

        self.assertEqual('GAME', table_name)
        if conn:
            conn.close()

        # Invalid Path - Check if correct error message is printed
        # if table already exists

        output = io.StringIO()
        sys.stdout = output
        db.init_db()
        sys.stdout = sys.__stdout__
        self.assertEqual('table GAME already exists\n', output.getvalue())

    def test_add_move(self):
        # Happy Path - Check if correct move is added to database
        db.reset_db()
        move = ('p2', "[[0, 0, 0, 0, 0, 0, 0],"
                      " [0, 0, 0, 0, 0, 0, 0], "
                      "[0, 0, 0, 0, 0, 0, 0], "
                      "['yellow', 0, 0, 0, 0, 0, 0], "
                      "['yellow', 'red', 0, 0, 0, 0, 0], "
                      "['yellow', 'red', 0, 0, 0, 0,"
                      " 0]]", '', 'yellow', 'red', 37)
        db.add_move(move)
        expected_move = db.getMove()
        self.assertEqual(move, expected_move)

        # Invalid Path - Check if correct error message is printed
        # if table does not exist and move is added to db
        db.clear()
        move = ('p2', "[[0, 0, 0, 0, 0, 0, 0],"
                      " [0, 0, 0, 0, 0, 0, 0], "
                      "[0, 0, 0, 0, 0, 0, 0], "
                      "['yellow', 0, 0, 0, 0, 0, 0], "
                      "['yellow', 'red', 0, 0, 0, 0, 0], "
                      "['yellow', 'red', 0, 0, 0, 0,"
                      " 0]]", '', 'yellow', 'red', 37)

        output = io.StringIO()
        sys.stdout = output
        db.add_move(move)
        sys.stdout = sys.__stdout__
        self.assertEqual('no such table: GAME\n', output.getvalue())

    def test_get_move(self):
        # Check if move is returned if data exists in database
        db.reset_db()
        move = ('p2', "[[0, 0, 0, 0, 0, 0, 0],"
                      " [0, 0, 0, 0, 0, 0, 0], "
                      "[0, 0, 0, 0, 0, 0, 0], "
                      "['yellow', 0, 0, 0, 0, 0, 0], "
                      "['yellow', 'red', 0, 0, 0, 0, 0], "
                      "['yellow', 'red', 0, 0, 0, 0,"
                      " 0]]", '', 'yellow', 'red', 37)
        db.add_move(move)
        self.assertTrue(db.getMove())

        # Check if None is returned if no data exists in database
        db.reset_db()
        self.assertIsNone(db.getMove())

        # Check if correct error message is printed if table does not exist
        db.clear()
        output = io.StringIO()
        sys.stdout = output
        db.getMove()
        sys.stdout = sys.__stdout__
        self.assertEqual('no such table: GAME\n', output.getvalue())

    def test_clear(self):
        # Check if GAME table is dropped
        db.clear()
        conn = sqlite3.connect('sqlite_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name FROM sqlite_master WHERE type=\'table\''
            ' AND name=\'GAME\';')

        rows = cursor.fetchone()
        self.assertIsNone(rows)
        if conn:
            conn.close()


if __name__ == '__main__':
    unittest.main()
