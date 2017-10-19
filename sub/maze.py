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
        self.cost = 1
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
                self.straight_maze.append(copy.deepcopy(row))

    def solve_straight_maze(self):
        self.straight_open_list.append(self.start)
        current = None
        while(len(self.goals)):
            goal = self.goals[0]
            current = self.find_least(open_list=self.straight_open_list)
            self.straight_open_list.remove(current)
            self.straight_closed_list.append(current)
            current.is_path = True
            self.calculate_straight_values(current, goal)
            if goal in self.straight_closed_list:
                self.goals.remove(goal)


    def find_least(self, open_list=[]):
        if open_list:
            open_list = sorted(open_list, key=lambda x: x.f, reverse=False)
            return open_list[0]
        return None

    def calculate_straight_values(self, current, goal):
        top = self.straight_maze[current.x - 1][current.y]
        down = self.straight_maze[current.x + 1][current.y]
        left = self.straight_maze[current.x][current.y - 1]
        right = self.straight_maze[current.x][current.y + 1]

        if top.s_type >= 0:
            top.parent = current
            top.set_h(h=self.straight_distance(top.x, top.y, goal.x, goal.y))
            top.set_g(g=current.g + self.cost)
            self.straight_open_list.append(top)

        if down.s_type >= 0:
            down.parent = current
            down.set_h(h=self.straight_distance(down.x, down.y, goal.x, goal.y))
            down.set_g(g=current.g + self.cost)
            self.straight_open_list.append(down)

        if left.s_type >= 0:
            left.parent = current
            left.set_h(h=self.straight_distance(left.x, left.y, goal.x, goal.y))
            left.set_g(g=current.g + left.cost)
            self.straight_open_list.append(left)

        if right.s_type >= 0:
            right.parent = current
            right.set_h(h=self.straight_distance(right.x, right.y, goal.x, goal.y))
            right.set_g(g=current.g + self.cost)
            self.straight_open_list.append(right)

    def straight_distance(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return self.cost * max(dx, dy)

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
