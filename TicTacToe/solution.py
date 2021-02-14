"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"
Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"
    [[-, -, o],
     [-, o, o],
     [x, x, x]]
     Return value should be "x wins!"
"""
from itertools import chain
from typing import List


def tic_tac_toe_checker(board: List[List]) -> str:
    n = len(board)
    board = list(chain.from_iterable(board))

    win_combs = []
    for i in range(0, n ** 2, n):
        win_combs.append(slice(i, i + n))  # add win rows

    for i in range(n):
        win_combs.append(slice(i, n ** 2, n))  # add win columns

    win_combs.append(slice(0, n ** 2, n + 1))  # add win diagonal
    win_combs.append(slice(n - 1, n ** 2 - 1, n - 1))  # add second win diagonal

    for comb in win_combs:
        comb_slice = board[comb]
        if len(set(comb_slice)) == 1 and "-" not in comb_slice:
            return f"{comb_slice[0]} wins!"
    return "draw!" if "-" not in board else "unfinished!"
