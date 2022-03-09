from cmath import inf
from enum import unique
import scipy.ndimage
import numpy as np

ROWS = 10
COLS = 6
board = np.zeros((ROWS, COLS), dtype=int)
pieces = [] # will be a list of lists of configurations for each piece
PIECE_FILE = "pieces.txt"


SMALLEST_PIECE_SIZE = 5  #TODO: find algorithmically


def load_pieces_from_file(piece_file_path):
    pieces_np = []
    with open(piece_file_path, 'r') as file:
        pieces_raw = {}
        pieces_count = 0
        lines = file.readlines()

        for line in lines:
            if line == "\n":
                pieces_count += 1
            else:
                if pieces_count not in pieces_raw:
                    pieces_raw[pieces_count] = []

                pieces_raw[pieces_count].append(line.strip())

        for i in range(0, pieces_count + 1):
            rows = len(pieces_raw[i])
            cols = max(len(x) for x in pieces_raw[i])
            piece_np = np.zeros((rows, cols), dtype=int)
            for r in range(0, rows):
                for c in range(0, cols):
                    piece_np[r,c] = int(pieces_raw[i][r][c])

            pieces_np.append(piece_np)

    return pieces_np


def generate_unique_piece_configurations(pieces):
    pieces_out = []
    for piece in pieces:
        all_configs = []
        all_configs.append(piece)
        for k in range(1,4):
            all_configs.append(np.rot90(piece, k))
        piece_flipped = np.flip(piece, axis=0)
        for k in range(0,4):
            all_configs.append(np.rot90(piece_flipped, k))
        
        unique_configs = []

        for config in all_configs:
            if not any(np.array_equal(config, unique_config) for unique_config in unique_configs):
                unique_configs.append(config)

        pieces_out.append(unique_configs)

    return pieces_out


def is_board_valid(board):
    # anti_board has 0s in occupied spaces, and 1s in empty spaces
    anti_board = 1 - board
    labeled_anti_board, _ = scipy.ndimage.label(anti_board)
    empty_spaces = scipy.ndimage.find_objects(labeled_anti_board)
    # if we find that there is contiguous empty region smaller than 5,
    # reject the board
    for slices in empty_spaces:
        if np.sum(anti_board[slices]) < SMALLEST_PIECE_SIZE:
            return False
    # We will check contiguous regions of the same size or higher if needed
    return True  # THIS MAY NOT BE RIGHT


def left_top_most_space(arr, is_board):
    if is_board:
        arr = 1 - arr
    best_y = inf
    best_x = inf
    # look for zeros
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            if arr[y,x] == 1:
                if x < best_x:
                    best_x = x
                    best_y = y
                elif x == best_x:
                    best_y = min(y, best_y)

            if best_x == 0:
                return (best_y, best_x)
    
    return (best_y, best_x)


def attempt_piece_placement(board, piece):
    succeeded = False

    board_coords = left_top_most_space(board, True)
    piece_coords = left_top_most_space(piece, False)

    # Check if we will go off the board
    board_rows = board.shape[0]
    board_cols = board.shape[1]
    piece_rows = board.shape[0]
    piece_cols = board.shape[1]

    if piece_coords[0] + piece_rows  > 

    return succeeded


def recursive_descent(board, pieces_left):
    return


def main():
    pieces = load_pieces_from_file("pieces.txt")
    unique_configs = generate_unique_piece_configurations(pieces)
    test_coords = left_top_most_space(unique_configs[4][0], False)
    return


if __name__ == "__main__":
    main()
