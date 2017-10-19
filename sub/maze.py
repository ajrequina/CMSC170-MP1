import copy
from square import Square
from operator import attrgetter


class Maze(object):
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.straight_maze = []
        self.straight_open_list = []
        self.straight_closed_list = []
        self.manhattan_maze = []
        self.manhattan_open_list = []
        self.manhattan_closed_list = []
        self.maze = []
        self.output = []
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
                self.output.append(chars)
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

                self.maze.append(copy.deepcopy(row))
    def perform_straight_maze(self): 
        while(len(self.goals)):
            pass

    def perform_manhattan_maze(self):
        maze = copy.deepcopy(self.maze)
        output = copy.deepcopy(self.output)

        def get_distance(start, end):
            return abs(start.x - end.x) + abs(start.y - end.y)

        def get_neighbors(current):
            ret_val = []
            max_width = len(maze[0])
            max_height = len(maze)
            temp_x = current.x
            temp_y = current.y
            if temp_x - 1 > 0 and abs(maze[temp_x - 1][temp_y].s_type) != 1:
                ret_val.append(maze[temp_x - 1][temp_y])
            if temp_x + 1 < max_height - 1 and abs(maze[temp_x + 1][temp_y].s_type) != 1:
                ret_val.append(maze[temp_x + 1][temp_y])
            if temp_y - 1 > 0 and abs(maze[temp_x][temp_y - 1].s_type) != 1:
                ret_val.append(maze[temp_x][temp_y - 1])
            if temp_y + 1 < max_width - 1 and abs(maze[temp_x][temp_y + 1].s_type) != 1:
                ret_val.append(maze[temp_x][temp_y + 1])
            return ret_val

        def create_path(current):
            file = open("manhattanBasic.txt", "w")
            # path = []
            while current.parent:
                output[current.x][current.y] = '.'
                current = current.parent
            output[current.x][current.y] = '.'
            for line in output:
                file.write("".join(line) + "\n")
            file.close

        open_list = []
        close_list = []
        start = maze[self.start.x][self.start.y]
        goal = maze[self.goals[0].x][self.goals[0].y]
        open_list.append(start)

        while open_list:
            min_open = open_list.index(min(open_list, key=attrgetter('f')))
            current = open_list.pop(min_open)
            neighbors = get_neighbors(current)

            for neighbor in neighbors:
                if neighbor.s_type == 2:
                    print(create_path(current))
                temp_g = current.g + get_distance(neighbor, current)
                temp_h = get_distance(neighbor, goal)
                temp_f = temp_g + temp_h

                if neighbor in close_list:
                    continue
                if neighbor in open_list:
                    if(neighbor.f > temp_f):
                        neighbor.f = temp_f
                    else :
                        continue
                else: 
                    neighbor.g = temp_g
                    neighbor.h = temp_h
                    neighbor.f = temp_f
                    open_list.append(neighbor)
                neighbor.parent = current
            close_list.append(current)
maze = Maze(file_name="../data/bigMaze.lay.txt")
maze.perform_manhattan_maze()
