
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
     is_path = will be set true if and only if the square is
               part of the path
     parent = the parent square of this square
    '''
    def __init__(self, x=0, y=0, s_type=0):
        self.x = x
        self.y = y
        self.s_type = s_type
        self.h = 0
        self.g = 0
        self.f = 0
        self.is_path = False
        self.parent = None


    def set_h(self, h=0):
        if self.h != 0 and h < self.h:
            self.h = h
            self.f = self.g + self.h

    def set_g(self, g=0):
        if self.g != 0 and g < self.g:
            self.g = g
            self.f = self.g + self.h
