from cmath import inf
from math import factorial
import copy
import scipy.ndimage
import numpy as np
import random

ROWS = 10
COLS = 6
board = np.zeros((ROWS, COLS), dtype=int)
pieces = [] # will be a list of lists of configurations for each piece
PIECE_FILE_PATH = "pieces.txt"
Total_Search_Space = 0
Remaining_Search_Space = 0
SOLNS_FILE_PATH = "solns.txt"
solns_found = 0

SMALLEST_PIECE_SIZE = 5  #TODO: find algorithmically

def convert_to_bitboard(board):
    bit_board = np.copy(board)
    bit_board[bit_board > 0] = 1
    return bit_board

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
    pieces_out = {}
    for i in range(len(pieces)):
        piece = pieces[i]
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

        pieces_out[i] = unique_configs

    return pieces_out


def is_board_valid(board):
    bit_board = convert_to_bitboard(board)
    # anti_board has 0s in occupied spaces, and 1s in empty spaces
    anti_bit_board = 1 - bit_board
    labeled_anti_board, _ = scipy.ndimage.label(anti_bit_board)
    empty_spaces = scipy.ndimage.find_objects(labeled_anti_board)
    # if we find that there is contiguous empty region smaller than 5,
    # reject the board
    for slices in empty_spaces:
        if np.sum(anti_bit_board[slices]) < SMALLEST_PIECE_SIZE:
            return False
    # We will check contiguous regions of the same size or higher if needed
    return True  # THIS MAY NOT BE RIGHT


def left_top_most_space(arr, is_board):
    if is_board:
        arr = convert_to_bitboard(arr)
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


def attempt_piece_placement(board, piece, piece_number):
    board_coords = left_top_most_space(board, True)
    piece_coords = left_top_most_space(piece, False)

    board_rows = board.shape[0]
    board_cols = board.shape[1]
    piece_rows = piece.shape[0]
    piece_cols = piece.shape[1]

    # Check if we will go off the board
    if board_coords[0] - piece_coords[0] not in range(0, board_rows)\
        or board_coords[0] + ((piece_rows - 1) - piece_coords[0]) not in range(0, board_rows)\
        or board_coords[1] - piece_coords[1] not in range(0, board_cols)\
        or board_coords[1] + ((piece_cols - 1) - piece_coords[1]) not in range(0, board_cols):
        return False, board

    # modified board
    mod_board = np.copy(board)

    # attempt to copy piece into the new board
    for i in range(piece_rows):
        for j in range(piece_cols):
            y = board_coords[0] + (i - piece_coords[0])
            x = board_coords[1] + (j - piece_coords[1])
            assert y >= 0 and x >= 0
            if piece[i,j] != 0 and mod_board[y,x] != 0:
                return False, board
            # this covers the conditions where mod_board[y,x] == 1 and piece[i,j] == 0, 
            # which would overwrite the board with a zero
            if piece[i,j] != 0:
                mod_board[y,x] = piece[i,j] * piece_number

    return True, mod_board

def search_space_size(unique_configs):
    size = factorial(len(unique_configs))
    for config_set in unique_configs.values():
        size *= len(config_set)

    return size

def recursive_descent(board, pieces_left, recursion_depth, solns_file):
    global Total_Search_Space
    global Remaining_Search_Space
    global solns_found
    if len(pieces_left) == 0:
        print("Solution found!")
        print(board)
        print("------------------------------")
        solns_file.write(str(board) + "\n")
        solns_file.write(str((Remaining_Search_Space/Total_Search_Space) * 100) + "%\n")
        solns_file.write("\n------------------------------\n")
        solns_file.flush()
        solns_found += 1
        if solns_found == 100:
            quit()
    for i in pieces_left.keys():
        for j in range(len(pieces_left[i])):
            config = pieces_left[i][j]
            succeeded, new_board = attempt_piece_placement(board, config, i + 1)
            new_pieces_left = pieces_left.copy() # This should be faster than copy.deepcopy 
                                                 # and we also don't need deep copy here
            new_pieces_left.pop(i)
            if succeeded and is_board_valid(new_board):
                recursive_descent(new_board, new_pieces_left, recursion_depth + 1, solns_file)
            else:
                Remaining_Search_Space -= search_space_size(new_pieces_left)
                #if random.randint(0,10000) == 10:
                    #print((Remaining_Search_Space/Total_Search_Space) * 100)

    return


def main():
    global Total_Search_Space
    global Remaining_Search_Space
    pieces = load_pieces_from_file("pieces.txt")
    unique_configs = generate_unique_piece_configurations(pieces)
    Total_Search_Space = search_space_size(unique_configs)
    Remaining_Search_Space = Total_Search_Space

    solns_file = open(SOLNS_FILE_PATH, "w")
    recursive_descent(board, unique_configs, 0, solns_file)

    return


if __name__ == "__main__":
    main()
