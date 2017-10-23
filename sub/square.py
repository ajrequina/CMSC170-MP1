
class Square(object):
    '''
     x = row index
     y = column index
     Square Types:
        -1 = wall
        0  = space
        1  = start
        2  = goal
     h = heuristic value
     g = path cost from the starting point
     f = h + g
     parent = the parent square of this square
    '''
    def __repr__(self):
        return str((str(self.x), str(self.y))) + " h = " + str(self.h) 

    def __init__(self, x=0, y=0, s_type=0):
        self.x = x
        self.y = y
        self.s_type = s_type
        self.h = 0
        self.g = 0
        self.f = 0
        self.parent = None