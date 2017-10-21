import copy
from square import Square
from operator import attrgetter


class Maze(object):
    def __init__(self, file_name=None, h_type="s"):
        self.file_name = file_name
        self.h_type = h_type
        self.close_list = []
        self.open_list = []
        self.maze = []
        self.output = []
        self.start = None
        self.goals = []
        self.path_cost = 1
        self.move_cost = 1
        self.frontier_size = 0
        self.generate()
        self.goal_count = len(self.goals)

    def generate(self):
        if self.file_name:
            maze = open("mazes/" + self.file_name, "r")
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

                self.maze.append(row)


    def get_neighbors(self, current):
        neighbors = []
        maze = self.maze
        max_width = len(maze[0])
        max_height = len(maze)
        temp_x = current.x
        temp_y = current.y

        # Top
        if temp_x - 1 > 0 and abs(maze[temp_x - 1][temp_y].s_type) != 1:
            neighbors.append(maze[temp_x - 1][temp_y])

        # Down
        if temp_x + 1 < max_height - 1 and abs(maze[temp_x + 1][temp_y].s_type) != 1:
            neighbors.append(maze[temp_x + 1][temp_y])

        # Left
        if temp_y - 1 > 0 and abs(maze[temp_x][temp_y - 1].s_type) != 1:
            neighbors.append(maze[temp_x][temp_y - 1])

        # Right
        if temp_y + 1 < max_width - 1 and abs(maze[temp_x][temp_y + 1].s_type) != 1:
            neighbors.append(maze[temp_x][temp_y + 1])

        return neighbors

    def find_least(self, open_list=[]):
        if open_list:
            open_list = sorted(open_list, key=lambda x: x.f, reverse=False)
            return open_list[0]
        return None


    def straight_distance(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return self.move_cost * max(dx, dy)


    def manhattan_distance(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return dx + dy

    def get_distance_single(self, start, goal):
        if self.h_type == "s":
            return self.straight_distance(
                    x1=start.x, y1=start.y,
                    x2=goal.x, y2=goal.y)

        elif self.h_type == "m":
            return self.manhattan_distance(
                    x1=start.x, y1=start.y,
                    x2=goal.x, y2=goal.y)

    def get_distance_multiple(self, start, goals=[]):
        if len(goals):
            heuristics = []

            for goal in goals:
                h = self.get_distance_single(start, goal)
                heuristics.append(h)

            return min(heuristics)

    def create_path(self, current):
        self.output[current.x][current.y] = str(self.goal_count)
        current = current.parent

        while current.parent:
            if self.output[current.x][current.y] == " ":
                self.output[current.x][current.y] = '.'
            self.path_cost += 1
            current = current.parent

        self.goal_count -= 1
        self.output[current.x][current.y] = str(self.goal_count)


    def write_output(self):
        o_name = self.file_name + "-" + self.h_type + "_dist.txt"
        file = open('mazes/solutions/' + o_name, "w")
        for line in self.output:
            file.write("".join(line) + "\n")
        file.write("COST: " + str(self.path_cost) + "\n")
        file.write("# of Expanded Nodes: " + str(len(self.close_list)) + "\n")
        file.write("Size of Frontiers: " + str(self.frontier_size))
        file.close()

    def solve(self):
        open_list = self.open_list
        close_list = self.close_list
        start = self.maze[self.start.x][self.start.y]
        open_list.append(start)
        frontier_size = self.frontier_size

        while len(self.goals):
            current = self.find_least(open_list=open_list)

            if len(open_list):
                open_list.remove(current)
            close_list.append(current)

            if current.s_type == 2 and current in self.goals:
                self.create_path(current)
                self.goals.remove(current)
                open_list.append(current)
                continue

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                temp_g = current.g + self.get_distance_single(neighbor, current)
                temp_h = self.get_distance_multiple(neighbor, self.goals)
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
                    self.frontier_size += 1
                neighbor.parent = current

        self.write_output()

