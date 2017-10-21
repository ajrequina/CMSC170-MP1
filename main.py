from sub.maze import Maze

class Main(object):
    def __init__(self):
        self.files = [
            'openMaze.lay.txt',
            'tinyMaze.lay.txt',
            'smallMaze.lay.txt',
            'mediumMaze.lay.txt',
            'bigMaze.lay.txt',
            'smallSearch.lay.txt',
            'mediumSearch.lay.txt',
            'bigSearch.lay.txt',
            'trickySearch.lay.txt'
        ]

        self.solve_mazes()

    def solve_mazes(self):
        for fname in self.files:
            maze = Maze(file_name=fname, h_type="s")
            maze.solve()

            maze = Maze(file_name=fname, h_type="m")
            maze.solve()

main = Main()
