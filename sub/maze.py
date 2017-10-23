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
        self.frontier_size = 1
        self.goal_len = 0
        self.generate()
        self.goal_count = 1
       
    '''
    Generates the maze from a file
    Sets the start position
    Sets the goals and contain it inside goals[]
    '''
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
                        self.goal_len += 1
                        self.goals.append(square)
                    y += 1
                    row.append(square)
                x += 1

                self.maze.append(row)

    '''
    Solves the given maze and put the solution inside output[]
    '''
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

            if current in self.goals:
                self.create_path(current)
                self.goals.remove(current)
                open_list.append(current)
                if len(self.goals):
                    current.h = 0
                    current.g = 0
                    current.f = current.h + current.g
                current.parent = None
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

    '''
    Helper function for solve()
    Return the neighbors(top, down, left, right) given a current square
    '''
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

    '''
    Helper function for solve()
    Returns the square with least f value given an open_list[]
    '''
    def find_least(self, open_list=[]):
        if open_list:
            open_list = sorted(open_list, key=lambda x: x.f, reverse=False)
            return open_list[0]
        return None


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

    '''
    Straight distance heuristics
    '''
    def straight_distance(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return self.move_cost * max(dx, dy)

    '''
    Manhattan distance heuristics
    '''
    def manhattan_distance(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return dx + dy

    '''
    Helper function for solve()
    Creates a path given a current square by tracking its parents
    Solves the path cost 
    '''
    def create_path(self, current):
        self.output[current.x][current.y] = str(self.goal_count)
        current = current.parent

        while True:
            self.path_cost += 1
            if self.output[current.x][current.y] == " ":
                self.output[current.x][current.y] = '.'
            if current.parent:
                current = current.parent
            else:
                break
       
        self.goal_count += 1

    '''
    Helper function for solve()
    Writes the output[] into a file
    Notes:
     - "m_dist.txt" (through Manhattan Distance heuristics) 
     - "s_dist.txt" (through Straight Distance heuristics)
    '''
    def write_output(self):
        o_name = self.file_name + "-" + self.h_type + "_dist.txt"
        file = open('mazes/solutions/' + o_name, "w")
        space_count = len(str(self.goal_len))
        space = ""
        if space_count > 0:
            space = " " * space_count
        for line in self.output:
            out_line = ""
            for char in line:
                out_line += char
                if not str(char).isdigit():
                    out_line += " " * space_count
                else:
                    out_line += " " + (" " * (space_count - (len(char))))

            file.write(out_line + "\n")

        file.write("COST: " + str(self.path_cost) + "\n")
        file.write("# of Expanded Nodes: " + str(len(self.close_list)) + "\n")
        file.write("Size of Frontiers: " + str(len(self.open_list)))
        file.close()

    

