#  Created by btrif Trif on 27-02-2023 , 10:27 PM.

import string, re
import numpy as np

maze_configuration1 = {
    "grid_size" : "8x8",
    "entrance" : "B2 ",
    "walls" : "C1, G1, A2, C2, E2,G2,C3,E3,B4,C4,E4,F4,G4,B5,E5,B6,D6,E6,G6,H6,B7,D7,G7,B8"
    }

maze_configuration2 = {
    "grid_size" : "8x8",
    "entrance" : "A1 ",
    "walls" : "C1,G1,A2,C2,E2,G2,E3,B4,E4,G4,D5,E5,H5,D6,H6,B6,D7,G7,H2"
    }


## CONVENTION : 0 - are Walls, 1 - is a valid square, 2 - is trace path ( been there )

class NotAValidEntrance(Exception) :
    """Raised when the input value is not 1 """
    pass


class MazeMapping() :
    '''Class to translate from maze configuration with strings and letters into matrix grid
        Important NOTE:     a position on a chess board (or excel )has the form (col, row)
        because col is always letter and row il always number. Therefore the pos :
        E2 (E is col, 2 is row)  -->   (row, col) = (1,  4)
    '''

    # __slots__ = ('grid_size', 'entrance', 'walls')

    def __init__(self, maze_config) :
        self.grid_size = maze_config[ 'grid_size' ]
        self.entrance = maze_config[ 'entrance' ]
        self.walls = maze_config[ 'walls' ]

        self.maze_matrix = self.get_maze_matrix_from_chess_config()
        self.maze_entrance = self.get_entrance()


    def get_maze_matrix_from_chess_config(self) :
        ''' Transforms the given maze configuration into computable matrix where
                0 is a free path  &      1 is a wall'''
        x, y = list(map(int, self.grid_size.split("x")))  # get row * cols sizes

        maze_grid = np.zeros(shape=(x, y), dtype=int)
        chars = {char : index for index, char in enumerate(string.ascii_uppercase)}
        # print(chars)
        self.walls = self.walls.replace(' ','')
        for wall in (self.walls).split(',') :
            letter, number = wall[ :1 ], int(wall[ 1 : ])  # here in B2, B is the column and 2 is the row
            print(f"wall : {wall},    column = {letter}  row = {number}        {(number - 1, chars[letter])}")
            maze_grid[ number - 1 ][ chars[ letter ] ] = 1  # row is number, col is letter
        print(f"final_maze : \n{maze_grid}")
        return maze_grid

    def get_entrance(self):
        ''' Translates from Entrance like C4 = (3, 2)   '''
        chars = {char : index for index, char in enumerate(string.ascii_uppercase)}
        print(f"entrance : {chars[ self.entrance[ :1 ] ], int(self.entrance[1:])-1 }")
        return ( int(self.entrance[1:])-1, chars[self.entrance[:1] ] )



def get_chess_table_from_matrix_form(maze_solution):
    chars = {index : char for index, char in enumerate(string.ascii_uppercase)}
    chess_solution = []
    for row, col in maze_solution :
        chess_solution.append( chars[col] + str(row+1) )
    print(f"chess sol : {chess_solution}")
    return ','.join(chess_solution)



class MazeDFS() :
    ''' the walls = 1, the paths = 0  '''

    def __init__(self, maze, start) :
        self.maze = maze
        self.start = start
        start_i, start_j = self.start
        print(f"start : {start_i}, {start_j}")
        self.all_found_paths = dict()
        self.path_so_far = [ ]
        self.get_next_move(start_i, start_j)
        self.longest_path = self.get_longest_path()


    def get_next_move(self, i, j) :  # the walls = 1, the paths = 0
        # check external limits of the maze
        if i < 0 or j < 0 or i > len(self.maze) - 1 or j > len(self.maze[ 0 ]) - 1 :
            return

        # If we've already been there or there is a wall, quit
        if (i, j) in self.path_so_far or self.maze[ i ][ j ] > 0 :
            return

        self.path_so_far.append((i, j))
        self.maze[ i ][ j ] = 2

        # Path found if we arrived at the bottom row :
        if i == len(self.maze) - 1 :
            # print(f"Found!   {self.path_so_far}")
            # print(f"moves :  {len(self.path_so_far)}")
            self.all_found_paths[len( self.path_so_far)] = self.path_so_far[:]
            return

        else :
            self.get_next_move(i - 1, j)  # check top
            self.get_next_move(i + 1, j)  # check bottom
            self.get_next_move(i, j + 1)  # check right
            self.get_next_move(i, j - 1)  # check left
        self.path_so_far.pop()

        # print(f'Longest path : { self.all_found_paths[ max(self.all_found_paths.keys()) ] }')

        return

    def get_longest_path(self):
        max_key = max( self.all_found_paths.keys() )
        return self.all_found_paths[ max_key ]


if __name__ == '__main__' :
    input_mapping = MazeMapping(maze_configuration1)
    maze_matrix = input_mapping.get_maze_matrix_from_chess_config()
    maze_entrance = input_mapping.get_entrance()
    print()

    solve_maze = MazeDFS(maze_matrix, maze_entrance )

    longest_path_solution = solve_maze.longest_path
    chess_solution = get_chess_table_from_matrix_form(longest_path_solution)
