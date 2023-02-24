#  Created by btrif Trif on 22-02-2023 , 10:56 AM.

import string, re
import numpy as np

maze_configuration = {
    "entrance": "B2 ",
    "gridSize": "8x8",
    "walls": "C1, G1, A2, C2, E2,G2,C3,E3,B4,C4,E4,F4,G4,B5,E5,B6,D6,E6,G6,H6,B7,D7,G7,B8"
    }

maze_configuration = {
    "entrance": "A1 ",
    "gridSize": "8x8",
    "walls": "C1,G1,A2,C2,E2,G2,E3,B4,E4,G4,D5,E5,H5,D6,H6,B6,D7,G7,H2"
    }


## CONVENTION : 0 - are Walls, 1 - is a valid square, 2 - is trace path ( been there )

class NotAValidEntrance(Exception):
    """Raised when the input value is not 1 """
    pass


class MazeGrid():
    def __init__(self, maze_config):
        self.config = maze_config
        self.maze = self.get_maze_from_config()
        self.entrance = self.get_entrance(self.config["entrance"])
        self.solutions = self.solve_maze_algorithm(self.maze, self.entrance)

    def get_entrance(self, entrance):
        letter = re.search('[A-Z]', entrance).group()
        col = string.ascii_uppercase.index(letter)
        return (0, col)

    def map_walls_to_matrix_indices(self):
        chars = {char: index for index, char in enumerate(string.ascii_uppercase)}
        # print(chars)
        Wall_indeces = []
        for wall in (self.config["walls"]).split(',') :
            letter, number = wall[:1], int(wall[1:])
            print(f"wall : {wall},    column = {letter}  row = {number} ")
            Wall_indeces.append((number - 1, chars[letter]))  # row is number, col is letter
        print(f"Wall_indeces : {Wall_indeces}")
        return Wall_indeces

    def get_maze_from_config(self):
        x, y = list(map(int, self.config["gridSize"].split("x")))

        maze = np.ones(shape=(x, y), dtype=int)
        wall_indeces = self.map_walls_to_matrix_indices()
        for x, y in wall_indeces:
            maze[x, y] = 0
        # print(f"final_maze :\n{maze}")
        return maze

    def translate_solution_into_letter_columns(self, solution):
        chars = {index: char for index, char in enumerate(string.ascii_uppercase)}
        chess_solution = []
        for row, col in solution:
            chess_solution.append(chars[col] + str(row + 1))
        return ','.join(chess_solution)

    def next_position(self, pos, move):
        ''' Get the next position'''
        pos = list(pos)
        if move == 'U': pos[0] -= 1  # ( i-1, j )      UP
        if move == 'R': pos[1] += 1  # ( i, j+1 )       RIGHT
        if move == 'D': pos[0] += 1  # ( i-1, j )        DOWN
        if move == 'L': pos[1] -= 1  # ( i, j-1 )            LEFT
        return tuple(pos)

    def is_valid_next_pos(self, pos, move, maze):
        ''' Check if the next_pos represents a valid move
        '''
        next_pos = self.next_position(pos, move)
        next_x, next_y = next_pos

        # Check x axis
        if not 0 <= next_x < len(maze):
            return False
        # Check y axis
        if not 0 <= next_y < len(maze[0]):
            return False
        # Check for wall or already been there
        if maze[next_x][next_y] == 0 or maze[next_x][next_y] == 2:
            return False

        return True

    def check_exit(self, maze, pos):
        ''' we arrive at the BOTTOM row, CASE in which is VALID MOVE and we have an EXIT, therefore a SOLUTION         '''
        if pos[0] == len(maze) - 1: return True

    def get_min_or_max_path(self, min_max):
        '''Arguments : min or max  '''
        len_paths = {k: len(v) for k, v in self.solutions.items()}
        min_key = min(len_paths, key=len_paths.get)
        max_key = max(len_paths, key=len_paths.get)
        # print(f"min_key = {min_key}      min_sol = {self.solutions[min_key]} ")
        # print(f"max_key = {max_key}      max_sol = {self.solutions[max_key]} ")
        min_solution = self.solutions[min_key]
        max_solution = self.solutions[max_key]
        if min_max == 'min':
            return self.translate_solution_into_letter_columns(min_solution)
        elif min_max == 'max':
            return self.translate_solution_into_letter_columns(max_solution)

    def solve_maze_algorithm(self, maze, entrance):
        '''
         A BFS-like Algorithm to find all possible paths of a MAZE from entrance to exit
        **©**  Written by Bogdan Trif @ 2022.07.10
            It is an EXPONENTIAL ALGO which is very slow for few walls as it finds all possible paths

            -- Description:
             By using a BFS approach it investigates all the unique  maze paths.
                - Entrance is always specified and is on the TOP ROW
                - Exit is not specified but it is always on the BOTTOM ROW.

                1. Starts with the Entrance, then computes the next steps.
                2. With every step a new path is added and iis passed to the Next iteration.
                3. Therefore with each iter of the main loop we will have a step ( position ) more.
                4. If a final path is found it is added to the Finalized Paths.

            -- FUTURE IMPROVEMENTS:

                For now the paths are kept in lists and when we search for a
                previous step we spend computing time of O(n).

                - Instead we could use a Dataclass to hold str --> as key,
                a list for an ordered path and a set() to search close to O(1) complexity
                and thus decrease search time.
                  '''

        if maze[entrance[0]][entrance[1]] == 0:
            raise NotAValidEntrance("You must use a valid Entrance")

        # print(f'pos :  {entrance}           {type(entrance)}')
        CompletePaths = {}
        cur_Paths = {'0': [entrance]}

        while len(cur_Paths) > 0:
            # for _ in range(12) :
            # print(f"cur_Paths : {cur_Paths}")
            # We need this dict  to hold the next Paths
            next_Paths = dict()
            for key, path in cur_Paths.items():
                # print(f"                    ~~   PATH = {path}           key = {key}    ~~~~ ")

                for move in ['U', 'R', 'D', 'L']:
                    # print(f"---- move =  {move} ")
                    pos = path[-1]
                    if self.is_valid_next_pos(pos, move, maze):
                        next_pos = self.next_position(pos, move)
                        # We add the new path only if we've not been there
                        if next_pos not in path:
                            # print(f'{move} accepted')
                            new_path = path.copy()
                            new_path.append(next_pos)
                            # print(f"pos = {pos},   move = {move},   next_pos = {next_pos} ,   new_path = {new_path}  ,    path = {path} ")
                            # Add the new path to the next_Paths, ONLY if regular move or EXIT move :
                            next_Paths[key + move] = new_path
                            # If we have an Exit then validate and ADD to the GENERAL Paths
                            if self.check_exit(maze, next_pos):
                                CompletePaths[key + move] = new_path
                                next_Paths.pop(key + move, None)

                            # print(f"inside next_Paths : {next_Paths}")
                    #     else:
                    #         print(f'{move} rejected ( already there ) ')
                    # else:
                    #     print(f'{move} declined')

            # print(f"cur_Paths : ")
            # for k,v in cur_Paths.items(): print(f"key = {k}       path = {v}")
            # print(f"next_Paths : ")
            # for k,v in next_Paths.items(): print(f"key = {k}       path = {v}")
            # print(f"next_Paths : {next_Paths}")
            # We prepare the next loop. So we take the new Paths on which we will work on
            cur_Paths = next_Paths.copy()

            # print('\n=========================')

        print(f'\nCompletePaths : ')
        for k, v in CompletePaths.items(): print(f'{k}     length={len(v)}      path : {v}')
        return CompletePaths


if __name__ == '__main__':
    solutions = MazeGrid(maze_configuration)
    print(solutions.solutions)
    min_or_max_sol = 'max'

    print(f"\n{min_or_max_sol} solution: {solutions.get_min_or_max_path(min_or_max_sol)}")

