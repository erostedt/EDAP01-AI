#!/usr/bin/python -u
"""
Reversi with Othello rules. 'B' corresponds to black and 'W' corresponds to white.
Author: Eric Rostedt
For the course EDAP01 - Artificial Intelligence
Lab 1
"""
# Imports
import pandas as pd
from copy import deepcopy
from time import time

BOARD_SIZE = 8


def construct_board():
    """
    Constructs a new board based on the Othello rules
    :return: New board
    """
    board = [[' ' for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]
    board[3][3], board[4][4] = 'W', 'W'
    board[3][4], board[4][3] = 'B', 'B'
    return board


def valid_move(player, r, c, board):
    """
    Checks if the move is valid.
    :param player: Which player
    :param r: The row
    :param c: The column
    :param board: current board
    :return: True if move is valid and a list of which tiles that should be flipped. False if move is invalid and in that case an empty list.
    """
    opponent = 'B' if player == 'W' else 'W'

    if board[r][c] != ' ' or not inside(r, c):
        return False, []

    row_check, row_flips = check_row(player, opponent, r, c, board)
    col_check, col_flips = check_col(player, opponent, r, c, board)
    diag1_check, diag1_flips = check_first_diag(player, opponent, r, c, board)
    diag2_check, diag2_flips = check_second_diag(player, opponent, r, c, board)
    return row_check or col_check or diag1_check or diag2_check, row_flips+col_flips+diag1_flips+diag2_flips


def inside(r, c):
    """
    Checks if the position is inside the board
    :param r: Row
    :param c: Column
    :return: True if inside board, else false.
    """
    return 0 <= r <= BOARD_SIZE-1 and 0 <= c <= BOARD_SIZE-1


def check_row(player, opponent, r, c, board):
    """
    Check if valid move along the row.
    :param player: Which player
    :param opponent: Which opponent
    :param r: The row
    :param c: The column
    :param board: current board
    :return: True with corresponding tiles to flip if move is valid, if move is invalid: returns false and empty list.
    """
    row = board[r]
    if player not in row:
        return False, []
    tiles_to_flip = []
    for col in range(BOARD_SIZE):
        if row[col] == player:
            # Go right
            if col < c:
                curr_col = col + 1
                all_opponents = True
                temp = []
                while curr_col < c:
                    if row[curr_col] != opponent:
                        all_opponents = False
                        break
                    temp.append((r, curr_col))
                    curr_col += 1
                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)

            # Go left
            elif c < col:
                curr_col = col - 1
                all_opponents = True
                temp = []
                while curr_col > c:
                    if row[curr_col] != opponent:
                        all_opponents = False
                        break
                    temp.append((r, curr_col))
                    curr_col -= 1
                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)

    if not tiles_to_flip:
        return False, []
    return True, tiles_to_flip


def check_col(player, opponent, r, c, board):
    """
        Check if valid move along the coumn.
        :param player: Which player
        :param opponent: Which opponent
        :param r: The row
        :param c: The column
        :param board: current board
        :return: True with corresponding tiles to flip if move is valid, if move is invalid: returns false and empty list.
        """
    col = [board[i][c] for i in range(BOARD_SIZE)]
    if player not in col:
        return False, []
    tiles_to_flip = []
    for row in range(BOARD_SIZE):
        if col[row] == player:
            # Go down
            if row + 1 < r:
                curr_row = row + 1
                all_opponents = True
                temp = []
                while curr_row < r:
                    if col[curr_row] != opponent:
                        all_opponents = False
                        break
                    temp.append((curr_row, c))
                    curr_row += 1
                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)

            # Go up
            elif r < row - 1:
                curr_row = row - 1
                all_opponents = True
                temp = []
                while curr_row > r:
                    if col[curr_row] != opponent:
                        all_opponents = False
                        break
                    temp.append((curr_row, c))
                    curr_row -= 1
                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)

    if not tiles_to_flip:
        return False, []
    return True, tiles_to_flip


def check_first_diag(player, opponent, r, c, board):
    """
        Check if valid move along the first diagonal.
        :param player: Which player
        :param opponent: Which opponent
        :param r: The row
        :param c: The column
        :param board: current board
        :return: True with corresponding tiles to flip if move is valid, if move is invalid: returns false and empty list.
        """
    r_it, c_it = r, c
    while r_it > 0 and c_it > 0:
        r_it -= 1
        c_it -= 1
    tiles_to_flip = []
    while r_it < BOARD_SIZE and c_it < BOARD_SIZE:
        if board[r_it][c_it] == player:
            if r < r_it and c < c_it:
                curr_r = r_it - 1
                curr_c = c_it - 1
                all_opponents = True
                temp = []
                while r < curr_r and c < curr_c:
                    if board[curr_r][curr_c] != opponent:
                        all_opponents = False
                        break
                    temp.append((curr_r, curr_c))
                    curr_r -= 1
                    curr_c -= 1

                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)

            elif r > r_it and c > c_it:
                curr_r = r_it + 1
                curr_c = c_it + 1
                all_opponents = True
                temp = []
                while r > curr_r and c > curr_c:
                    if board[curr_r][curr_c] != opponent:
                        all_opponents = False
                        break
                    temp.append((curr_r, curr_c))
                    curr_r += 1
                    curr_c += 1

                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)
        r_it += 1
        c_it += 1

    if not tiles_to_flip:
        return False, []
    return True, tiles_to_flip


def check_second_diag(player, opponent, r, c, board):
    """
        Check if valid move along the second diagonal.
        :param player: Which player
        :param opponent: Which opponent
        :param r: The row
        :param c: The column
        :param board: current board
        :return: True with corresponding tiles to flip if move is valid, if move is invalid: returns false and empty list.
        """
    r_it, c_it = r, c
    while r_it < BOARD_SIZE - 1 and c_it > 0:
        r_it += 1
        c_it -= 1
    tiles_to_flip = []
    while r_it >= 0 and c_it < BOARD_SIZE:
        if board[r_it][c_it] == player:
            if r > r_it and c < c_it:
                curr_r = r_it + 1
                curr_c = c_it - 1
                all_opponents = True
                temp = []
                while r > curr_r and c < curr_c:
                    if board[curr_r][curr_c] != opponent:
                        all_opponents = False
                        break
                    temp.append((curr_r, curr_c))
                    curr_r += 1
                    curr_c -= 1

                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)

            elif r < r_it and c > c_it:
                curr_r = r_it - 1
                curr_c = c_it + 1
                all_opponents = True
                temp = []
                while r < curr_r and c > curr_c:
                    if board[curr_r][curr_c] != opponent:
                        all_opponents = False
                        break
                    temp.append((curr_r, curr_c))
                    curr_r -= 1
                    curr_c += 1

                if all_opponents:
                    for coordinate in temp:
                        tiles_to_flip.append(coordinate)
        r_it -= 1
        c_it += 1

    if not tiles_to_flip:
        return False, []
    return True, tiles_to_flip


def max_function(player, board):
    """
    Function that computer tries to maximize. The function is defined as number of current players tiles - number of opponents tiles
    :param player: Current player
    :param board: current board
    :return: score for player with respect to the function.
    """
    opponent = 'B' if player == 'W' else 'W'
    player_score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player:
                player_score += 1
            elif board[row][col] == opponent:
                player_score -= 1
    return player_score


def final_score(player, board):
    """
        Calculates the amount of tiles a given player has.
        :param player: Current player
        :param board: current board
        :return: tiles in ownership of player.
        """
    player_final_score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player:
                player_final_score += 1
    return player_final_score


def get_possible_moves(player, board):
    """
    Finds all possible moves.
    :param player: Current player
    :param board: Current board
    :return: all possible moves for player
    """
    possible_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            possible_move, _ = valid_move(player, row, col, board)
            if possible_move:
                possible_moves.append((row, col))
    return possible_moves


def make_move(player, r, c, board):
    """
    Makes a move if the move is valid.
    :param player: Current player
    :param r: Row
    :param c: Column
    :param board: Current board
    :return: Updated board
    """
    valid, tiles_to_flip = valid_move(player, r, c, board)
    if valid:
        board[r][c] = player
        for (row, col) in tiles_to_flip:
            board[row][col] = player
    return board


def done(player, board):
    """
    Checks if game is over.
    :param player: Current player
    :param board: Current board
    :return: True if game is over, false else.
    """
    if not get_possible_moves(player, board):
        return True
    return False


def alphabeta(board, initial_depth, depth, alpha, beta, maximizing_player, player, best_move, init_time, max_time):
    """
    Alpha-beta pruning in combination with minmax algorithm.
    :param board: current board
    :param initial_depth: how deep the tree is
    :param depth: current depth
    :param alpha: alpha parameter for alpha beta pruning
    :param beta: beta parameter for alpha beta pruning
    :param maximizing_player: True if player is maximizing, false else.
    :param player: Current player
    :param best_move: current best move
    :param init_time: initial time
    :param max_time: max tolerated time for the algorithm
    :return: best move given algorithm
    """
    if time() - init_time > max_time:
        return -10000, best_move
    if depth == 0 or done(player, board):
        return max_function(player, board), []

    if maximizing_player:
        max_eval = -10000
        for move in get_possible_moves(player, board):
            board = make_move(player, move[0], move[1], board)
            val, _ = alphabeta(board, initial_depth, depth - 1, alpha, beta, False, change_player(player), best_move, init_time, max_time)
            if depth == initial_depth:
                if val > max_eval:
                    best_move = move
            max_eval = max(max_eval, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 10000
        for move in get_possible_moves(player, board):
            board = make_move(player, move[0], move[1], board)
            val, _ = alphabeta(board, initial_depth, depth - 1, alpha, beta, True, change_player(player), best_move, init_time, max_time)
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval, []


def display(board):
    """
    Prints current board state
    :param board: current board
    """
    for row in board:
        print(row)


def change_player(player):
    """
    Changes player
    :param player: Current player
    :return: Other player
    """
    if player == 'W':
        return 'B'
    return 'W'


def play():
    """
    Plays a game of reversi, where a human plays against a computer algorithm.
    """
    board = construct_board()
    human_player = input('Welcome to Othello. Please Type B for black (upper case) or anything else for white: \n')
    select_depth = input('Difficulty is set on hard by default, to change difficulty type: y. Press any other key to keep hard difficulty. \n')
    if select_depth.lower() == 'y':
        depth = 6
        while depth > 5 or depth < 1:
            try:
                depth = int(input('Select difficulty: 1 for Super Easy, 2 for Easy, 3 for medium, 4 for hard, 5 for super hard: \n'))
                if depth > 5 or depth < 1:
                    print('Must be integer between 1 and 5.')
            except ValueError:
                print('Must be an integer.')

    else:
        depth = 4

    time_limit = input('Do you want a time limit for the computer? If so, press: y. Otherwise press any key\n')
    if time_limit.lower() == 'y':
        time_limit = -1
        while time_limit < 0 or time_limit > 1_000_000:
            try:
                time_limit = int(input('Select a time limit: 1 - 1 000 000 (ms). (NB! Being to restrictive on the difficulty may alter the difficulty). \n'))/1000
            except ValueError:
                print('Must be an integer in the appropriate range')
    else:
        time_limit = 100

    if human_player != 'B':
        human_player = 'W'
        computer = 'B'
    else:
        computer = 'W'

    game_over = False
    player = human_player if human_player == 'B' else computer
    while not game_over:
        print('Current Board state: ')
        display(board)
        if player == human_player:
            possible_moves = get_possible_moves(player, board)
            move_pool = len(possible_moves)-1
            pick = move_pool + 1
            while pick > move_pool or pick < 0:
                print('Humans turn, possible moves are: {}'.format(possible_moves))
                pick = int(input('Pick a choice: (0-{})\n'.format(move_pool)))
                if pick > move_pool or pick < 0:
                    print('Must choose between: (0-{})'.format(move_pool))
            move = possible_moves[pick]
            print('Your move was: {}'.format(move))
            board = make_move(player, move[0], move[1], board)
        else:
            best_move = get_possible_moves(player, board)[0]
            _, best_move = alphabeta(deepcopy(board), depth, depth, -10000, 10000, True, player, best_move, time(), time_limit)
            print('Computers move was move was: {}'.format(best_move))
            board = make_move(player, best_move[0], best_move[1], board)

        player = change_player(player)
        game_over = done(player, board)
    print('Game is over.')
    human_final_score, computer_final_score = final_score(human_player, board), final_score(computer, board)
    print('Human player got: {}, Computer got: {}'.format(human_final_score, computer_final_score))
    if human_final_score > computer_final_score:
        print('Human wins')
    elif computer_final_score > human_final_score:
        print('Computer wins')
    else:
        print('Draw')
    print('Thanks for playing Reversi!')


if __name__ == '__main__':
    play()
