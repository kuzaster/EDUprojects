from solution import tic_tac_toe_checker


def test_tic_tac_toe_checker_with_winner_row():
    board = [["-", "-", "o"], ["-", "o", "o"], ["x", "x", "x"]]
    assert tic_tac_toe_checker(board) == "x wins!"


def test_tic_tac_toe_checker_with_winner_column():
    board = [["-", "-", "o"], ["-", "x", "o"], ["x", "x", "o"]]
    assert tic_tac_toe_checker(board) == "o wins!"


def test_tic_tac_toe_checker_with_winner_diagonal():
    board = [["x", "-", "o"], ["-", "x", "o"], ["o", "o", "x"]]
    assert tic_tac_toe_checker(board) == "x wins!"


def test_tic_tac_toe_checker_with_winner_second_diagonal():
    board = [["x", "-", "o"], ["-", "o", "o"], ["o", "o", "x"]]
    assert tic_tac_toe_checker(board) == "o wins!"


def test_tic_tac_toe_checker_with_draw():
    board = [["o", "x", "o"], ["x", "o", "o"], ["x", "o", "x"]]
    assert tic_tac_toe_checker(board) == "draw!"


def test_tic_tac_toe_checker_with_unfinished():
    board = [["-", "-", "o"], ["-", "o", "o"], ["x", "o", "x"]]
    assert tic_tac_toe_checker(board) == "unfinished!"


def test_4x4_tic_tac_toe_checker_with_winner_row():
    board = [
        ["o", "x", "o", "o"],
        ["o", "-", "-", "o"],
        ["x", "x", "x", "x"],
        ["o", "o", "-", "x"],
    ]
    assert tic_tac_toe_checker(board) == "x wins!"


def test_4x4_tic_tac_toe_checker_with_winner_column():
    board = [
        ["o", "x", "o", "o"],
        ["o", "-", "-", "o"],
        ["o", "x", "o", "x"],
        ["o", "o", "-", "x"],
    ]
    assert tic_tac_toe_checker(board) == "o wins!"


def test_4x4_tic_tac_toe_checker_with_winner_diagonal():
    board = [
        ["x", "x", "o", "o"],
        ["o", "x", "-", "o"],
        ["o", "-", "x", "x"],
        ["o", "o", "-", "x"],
    ]
    assert tic_tac_toe_checker(board) == "x wins!"


def test_4x4_tic_tac_toe_checker_with_winner_second_diagonal():
    board = [
        ["x", "x", "o", "o"],
        ["o", "-", "o", "o"],
        ["o", "o", "x", "x"],
        ["o", "o", "-", "x"],
    ]
    assert tic_tac_toe_checker(board) == "o wins!"


def test_4x4_tic_tac_toe_checker_with_draw():
    board = [
        ["x", "x", "o", "o"],
        ["o", "x", "x", "o"],
        ["o", "o", "o", "x"],
        ["o", "o", "o", "x"],
    ]
    assert tic_tac_toe_checker(board) == "draw!"


def test_4x4_tic_tac_toe_checker_with_unfinished():
    board = [
        ["-", "x", "o", "o"],
        ["o", "x", "-", "o"],
        ["o", "-", "o", "x"],
        ["o", "o", "o", "x"],
    ]
    assert tic_tac_toe_checker(board) == "unfinished!"
