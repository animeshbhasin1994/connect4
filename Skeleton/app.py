import json
import logging
from flask import Flask, render_template, request, jsonify
# from flask import redirect
# from json import dump
from Gameboard import Gameboard
# import db


app = Flask(__name__)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None
game = Gameboard()
'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    game.reset_game()
    return render_template('player1_connect.html', status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    status = request.args.get('color', '')
    game.set_player_color('p1', status)
    return render_template('player1_connect.html', status=status)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if game.player1 == 'red':
        game.set_player_color('p2', 'yellow')
    elif game.player1 == 'yellow':
        game.set_player_color('p2', 'red')
    else:
        game.set_player_color('p2', 'Please wait for p1 to select color')
    return render_template('p2Join.html', status=game.player2)


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    invalid_reason = game.get_error_move_reason(current_turn='p1')

    if invalid_reason:
        return jsonify(move=game.board, invalid=True,
                       winner=game.game_result, reason=invalid_reason)

    else:
        data = request.get_data()
        data = json.loads(str(data.decode('utf-8')))
        col = data['column']
        col_no = int(col[-1]) - 1
        invalid_reason = game.get_column_full_error(col_no)
        if invalid_reason:
            return jsonify(move=game.board, invalid=True,
                           winner=game.game_result, reason=invalid_reason)

        invalid_flag = False
        row_idx = game.next_move_row_index(col_no)

        game.make_p1_move(row_idx, col_no)
        game.check_game_over(game.player1)
        return jsonify(move=game.board, invalid=invalid_flag,
                       winner=game.game_result)


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    invalid_reason = game.get_error_move_reason(current_turn='p2')

    if invalid_reason:
        return jsonify(move=game.board, invalid=True,
                       winner=game.game_result, reason=invalid_reason)

    else:
        data = request.get_data()
        data = json.loads(str(data.decode('utf-8')))
        col = data['column']
        col_no = int(col[-1]) - 1
        invalid_reason = game.get_column_full_error(col_no)
        if invalid_reason:
            return jsonify(move=game.board, invalid=True,
                           winner=game.game_result, reason=invalid_reason)

        invalid_flag = False
        row_idx = game.next_move_row_index(col_no)

        game.make_p2_move(row_idx, col_no)
        game.check_game_over(game.player2)
        return jsonify(move=game.board, invalid=invalid_flag,
                       winner=game.game_result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
