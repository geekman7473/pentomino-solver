import scipy.ndimage
import numpy as np

ROWS = 10
COLS = 6
board = np.zeros((ROWS, COLS), dtype=int)
pieces = []
PIECE_FILE = "pieces.txt"


SMALLEST_PIECE_SIZE = 5  #TODO: find algorithmically


def load_pieces_from_file(piece_file):
    return


def generate_piece_configurations(pieces):
    return


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


def attempt_piece_placement(board, piece):
    return


def recursive_descent(board, pieces_left):
    return


def main():
    return


if __name__ == "__main__":
    main()
