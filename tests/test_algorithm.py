#  Created by btrif Trif on 25-02-2023 , 8:27 PM.


from src.mazes.algorithms import MazeDFS, MazeMapping


def test_MazeDFS():


    grid_config1 = {'grid_size': '10x7', 'walls': 'B2,C3,A4,A5,B6,B3,C10,E1,F7,A10', 'entrance': 'C1'}

    grid_config2= {'grid_size': '15x14',
                   'walls': 'J7,L4,K8,K9,G11,E9,N15,A11,L1,D2,F12,J15,A5,C3,E13,L12,M7,A14,C11,I7,D1,J4,J13,A2,N11,H10,H8,G13,N12,H7,B12,J5,C9,A4,N2,J14,N9,A7,L13,E6,H4,K13,B3,F9,D5,E4,M9,N3,G4,N1,G15,D15,I13,F6,D8,I11,N8,E8,H3,H2,K6,B8,N10,I9,K4,N14,L15,G2,K3,M4,D9,F3,B4,H1,L10,J12,I1,C15,F14,F1,C12,G9,F11,C4,K1,J9,B15,G7,D10,J8,B7',
                   'entrance': 'I1'}

    input_mapping = MazeMapping(grid_config2)
    maze_matrix = input_mapping.get_maze_matrix_from_chess_config()
    maze_entrance = input_mapping.get_entrance()

    min_maze_solution = MazeDFS(maze_matrix, maze_entrance).longest_path

    print(min_maze_solution)
