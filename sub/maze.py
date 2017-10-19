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
        self.cost = 1
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

maze = Maze(file_name="../data/openMaze.lay.txt")
