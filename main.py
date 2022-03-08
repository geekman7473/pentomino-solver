import scipy.ndimage
import numpy as np

rows = 10
cols = 6
board = np.zeros((rows,cols), dtype=int)

def isBoardValid(board, pieces):
    #anti_board has 0s in occupied spaces, and 1s in empty spaces
anti_board = 1 - board
labeled_anti_board, num_labels = scipy.ndimage.label(anti_board)
empty_spaces = scipy.ndimage.find_objects(labeled_anti_board)

    
