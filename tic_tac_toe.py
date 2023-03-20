from typing import TypeVar

T = TypeVar("T", int, int)


def get_cell_position(cell_str: str) -> tuple[T, T]:
    # Convert the letter part of the cell string to a column index
    column_index = ord(cell_str[0]) - ord("A")

    # Convert the digit part of the cell string to a row index
    row_index = int(cell_str[1]) - 1

    # Return the row and column indices as a tuple
    return (row_index, column_index)


def tic_tac_toe() -> tuple[T, T]:
    board = [
        (" ", " ", "O"),
        ("X", " ", " "),
        (" ", " ", "X"),
    ]

    cell_str = "C1"
    row, col = get_cell_position(cell_str)
    if board[row][col] == "X":
        print("There is an X in cell", cell_str)
    elif board[row][col] == "O":
        print("There is an O in cell", cell_str)
    else:
        print("There is no X or O in cell", cell_str)
    return (row, col)


tic_tac_toe()
