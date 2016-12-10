"""
A functional implementation of Conway's Game of Life.

Written for Nic Wolf's Development Basics TouchDesigner workshop.

Author
----------
Nicholas Wolf

"""

import numpy as np


def create_board(height, width, p_alive):
    """
    This function creates a Game of Life game board.
    
    Parameters
    ----------
        height : integer
            the height of the board
        width : integer
            the width of the board
        p_alive : float
            the chance that a cell is set to 'alive', must be in [0, 1]
            
    Returns
    ----------
        board : 2d array
            a Game of Life board, with 'living' and 'dead' cells
    
    Examples
    ----------
    >>> np.random.seed(1)
    >>> create_board(3, 3, .3)
    array([[0, 1, 0],           
           [0, 0, 0],
           [0, 0, 0]])
    """
    dead, alive = 0, 1
    p_dead = 1 - p_alive # We know that if a cell is not alive, it must be dead
    board = np.random.choice([dead, alive], p=[p_dead, p_alive], size=(height, width))
    
    return board


def count_living_neighbors(board, r, c):
    """
    Counts the number of living neighbors around an array cell.
    
    Parameters
    ----------
        board : 2d array
        r : int
            row index
        c : int
            column index
            
    Returns
    ----------
        int
            number of living neighbors

    """
    num_rows, num_cols = board.shape
    
    u_ = board[(r-1) % num_rows, c % num_cols]
    d_ = board[(r+1) % num_rows, c % num_cols]
    l_ = board[r % num_rows, (c-1) % num_cols]
    r_ = board[r % num_rows, (c+1) % num_cols]
    ul = board[(r-1) % num_rows, (c-1) % num_cols]
    ur = board[(r-1) % num_rows, (c+1) % num_cols]
    dl = board[(r+1) % num_rows, (c-1) % num_cols]
    dr = board[(r+1) % num_rows, (c+1) % num_cols]
    
    return (u_ + d_ + l_ + r_ + ul + ur + dl + dr)

def compute_next_state(current_state, num_living_neighbors):
    """
    Computes the state of a cell in the next generation of a Game of Life.
    
    Parameters
    ----------
        current_state : int
        num_living_neighbors : int
        
    Returns
    ----------
        next_state : int
        
    """
    dead, alive = 0, 1
    next_state = dead
    
    if (num_living_neighbors < 2) and (current_state == alive):
        # Dies by under-population
        next_state = dead
    elif ( 2 <= num_living_neighbors <= 3) and (current_state == alive):
        # Survives on to the next generation
        next_state = alive
    elif (num_living_neighbors > 3) and (current_state == alive):
        # Dies by over-population
        next_state = dead
    elif (num_living_neighbors == 3) and (current_state == dead):
        # Live cell is birthed 
        next_state = alive
    
    return next_state

def step_forward(board):
    """
    Computes the next generation of a Game of Life board.
    
    Parameters
    ----------
        board : 2d array
        
    Returns
    ----------
        next_board : 2d array
    """
    # Copy the current board for the next generation
    next_board = board.copy()
    # Loop over all of the cells in the current board
    rows, cols = board.shape
    for r in range(rows):
        for c in range(cols):
            # Fetch the current state of this cell
            current_state = board[r, c]
            # Count the number of living neighbors
            num_living_neighbors = count_living_neighbors(board, r, c)
            # Figure out if this cell will be alive or dead in the next board
            next_state = compute_next_state(current_state, num_living_neighbors)
            # Set the state of this cell in the next board
            next_board[r, c] = next_state  
    
    return next_board

def main():
    # Test everything out to see if it works.
    # Create a new board
    board = create_board(5, 5, .3)
    print('Starting:')
    print(board)

    # Step the board forward a generation
    print('Next Step:')
    board = step_forward(board)
    print(board)
    
if __name__ == '__main__':
    main()    