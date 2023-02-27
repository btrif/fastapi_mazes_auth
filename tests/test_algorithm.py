#  Created by btrif Trif on 25-02-2023 , 8:27 PM.


from src.mazes.algorithms import MazeGrid


def test_MazeGrid():


    grid_config = {'grid_size': '10x7', 'walls': 'B2,C3,A4,A5,B6,B3,C10,E1,F7,A10', 'entrance': 'C1'}

    min_maze_solution = MazeGrid(grid_config).get_min_or_max_path('min')

    print(min_maze_solution)
