#  Created by btrif Trif on 27-02-2023 , 10:27 PM.

import string, re
import numpy as np

maze_configuration = {
    "grid_size": "8x8",
    "entrance": "B2 ",
    "walls": "C1, G1, A2, C2, E2,G2,C3,E3,B4,C4,E4,F4,G4,B5,E5,B6,D6,E6,G6,H6,B7,D7,G7,B8"
    }

maze_configuration = {
    "grid_size": "8x8",
    "entrance": "A1 ",
    "walls": "C1,G1,A2,C2,E2,G2,E3,B4,E4,G4,D5,E5,H5,D6,H6,B6,D7,G7,H2"
    }


## CONVENTION : 0 - are Walls, 1 - is a valid square, 2 - is trace path ( been there )

class NotAValidEntrance(Exception):
    """Raised when the input value is not 1 """
    pass


class ChessTableToGridMapping():
    '''Class to translate from maze configuration with strings and letters into matrix grid'''

    # __slots__ = ('grid_size', 'entrance', 'walls')

    def __init__(self, maze_config):
        self.grid_size = maze_config['grid_size']
        self.entrance = maze_config['entrance']
        self.walls = maze_config['walls']


    def translate_coord(self):
        pass


    def get_grid_from_chess(self):
        pass


    def get_chess_from_grid(self):
        pass



    def get_maze_matrix_from_chess_config(self):
        ''' Transforms the given maze configuration into computable matrix where
                1 is a free path  &      0 is a wall'''
        x, y = list(map(int, self.grid_size.split("x")))  # get row * cols sizes

        maze_grid = np.ones(shape=(x, y), dtype=int)
        # print(maze_grid)
        chars = {char: index for index, char in enumerate(string.ascii_uppercase)}


        for wall in (self.walls).split(',') :
            letter, number = wall[:1], int(wall[1:])            # here in B2, B is the column and 2 is the row
            # print(f"wall : {wall},    column = {letter}  row = {number}        {(number - 1, chars[letter])}")
            maze_grid[number-1][chars[letter]] = 0          # row is number, col is letter
        print(f"final_maze : \n{maze_grid}")
        return maze_grid


if __name__ == '__main__':
    CTTGM = ChessTableToGridMapping(maze_configuration)
    maze_matrix = CTTGM.get_maze_matrix_from_chess_config()
    print()

