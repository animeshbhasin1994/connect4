import sqlite3
from sqlite3 import Error

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('delete from GAME;')
        sql_string = '''insert into GAME values ('{}', "{}", '{}',
            '{}', '{}', {});''' \
            .format(move[0], str(move[1]), move[2], move[3], move[4],
                    move[5])
        conn.execute(sql_string)
        conn.commit()
        print('Move record, record inserted')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    # will return tuple(current_turn, board, winner, player1, player2,
    # remaining_moves) or None if db fails
    try:
        conn = sqlite3.connect('sqlite_db')
        cursor = conn.cursor()
        cursor.execute('''select * from GAME ;''')
        rows = cursor.fetchall()
        print(rows)
        if rows:
            print('Get record, record fetched')
            return rows[0]
        else:
            print('No move found')
            return None

    except Error as e:
        return None
        print(e)

    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def reset_db():
    clear()
    init_db()
