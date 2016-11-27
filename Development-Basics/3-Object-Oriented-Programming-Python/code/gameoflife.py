"""
An Object Oriented implementation of Conway's Game of Life.

Written for Nic Wolf's Development Basics TouchDesigner workshop.

Author
----------
Nicholas Wolf

"""

import numpy as np

class GameOfLife:
    """Conway's Game of Life"""
    DEAD, ALIVE = 0, 1
    def __init__(self):
        """Initialize a class instance"""
        self.board = None
        
    def is_empty(self):
        """Check to see if the Game of Life board is empty"""
        return (self.board == 0).all()
    
    def restart(self, height, width, p_alive):
        """Restart the Game of Life simulation with a new board"""
        self.board = self.new_board(height, width, p_alive)
    
    def start(self, height, width, p_alive=.3):
        """Start a new simulation."""
        self.new_board(height, width, p_alive)
    
    def step(self):
        """Step the simulation forward a generation."""
        # Copy the current board for the next generation
        next_board = self.board.copy()
        # Loop over all of the cells in the current board
        num_rows, num_cols = self.board.shape
        for r in range(num_rows):
            for c in range(num_cols):
                # Fetch the current state of this cell
                current_state = self.board[r, c]
                # Count the number of living neighbors
                num_living_neighbors = self.count_living_neighbors(r, c)
                # Figure out if this cell will be alive or dead in the next board
                next_state = self.compute_next_state(current_state, num_living_neighbors)
    #             next_state = 1
                # Set the state of this cell in the next board
                next_board[r, c] = next_state  

        self.board = next_board
    
    def is_empty(self):
        """Check to see if the Game of Life board is empty"""
        pass
    
    def new_board(self, height, width, p_alive):
        """
        This function creates a Game of Life game board.

        Parameters
        ----------
            height : integer
                the height of the board
            width : integer
                the width of the board
            p_alive : float
                the chance that a cell is set to 'alive', must be between [0, 1]
                
        """
        dead, alive = 0, 1
        p_dead = 1 - p_alive # We know that if a cell is not alive, it must be dead
        self.board = np.random.choice(
            [self.DEAD, self.ALIVE], p=[p_dead, p_alive], size=(height, width)
        )

    def count_living_neighbors(self, r, c):
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
        num_rows, num_cols = self.board.shape

        u_ = self.board[(r-1) % num_rows, c % num_cols]
        d_ = self.board[(r+1) % num_rows, c % num_cols]
        l_ = self.board[r % num_rows, (c-1) % num_cols]
        r_ = self.board[r % num_rows, (c+1) % num_cols]
        ul = self.board[(r-1) % num_rows, (c-1) % num_cols]
        ur = self.board[(r-1) % num_rows, (c+1) % num_cols]
        dl = self.board[(r+1) % num_rows, (c-1) % num_cols]
        dr = self.board[(r+1) % num_rows, (c+1) % num_cols]

        return (u_ + d_ + l_ + r_ + ul + ur + dl + dr)

    def compute_next_state(self, current_state, num_living_neighbors):
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
        next_state = self.DEAD

        if (num_living_neighbors < 2) and (current_state == self.ALIVE):
            # Dies by under-population
            next_state = self.DEAD
        elif ( 2 <= num_living_neighbors <= 3) and (current_state == self.ALIVE):
            # Survives on to the next generation
            next_state = self.ALIVE
        elif (num_living_neighbors > 3) and (current_state == self.ALIVE):
            # Dies by over-population
            next_state = self.DEAD
        elif (num_living_neighbors == 3) and (current_state == self.DEAD):
            # Live cell is birthed 
            next_state = self.ALIVE

        return next_state