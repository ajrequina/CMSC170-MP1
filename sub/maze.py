import copy
from square import Square


class Maze(object):
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.straight_maze = []
        self.straight_open_list = []
        self.straight_closed_list = []
        self.manhattan_maze = []
        self.manhattan_open_list = []
        self.manhattan_closed_list = []
        self.start = None
        self.goals = []
        self.generate()

    def generate(self):
        if self.file_name:
            maze = open(self.file_name, "r")
            x = 0
            for line in maze:
                line = line.replace('\n', '').replace('\r', '')
                chars = list(line)

                row = []
                y = 0
                for char in chars:
                    square = None
                    if char == "%":
                        square = Square(x=x, y=y, s_type=-1)
                    elif char == " ":
                        square = Square(x=x, y=y, s_type=0)
                    elif char == "P":
                        square = Square(x=x, y=y, s_type=1)
                        self.start = square
                    elif char == ".":
                        square = Square(x=x, y=y, s_type=2)
                        self.goals.append(square)

                    y += 1
                    row.append(square)
                x += 1

                self.straight_maze.append(copy.deepcopy(row))
                self.manhattan_maze.append(copy.deepcopy(row))

    def perform_straight_maze(self):
        while(len(self.goals)):
            pass

    def calculate_

maze = Maze(file_name="../data/openMaze.lay.txt")
