from .cube import Cube
from .patterns import Patterns

class Cube_AI(Cube):
    def __init__(self, size, time = 0.1, do_print = False):
        super().__init__(size, time, do_print)
        self.patterns = Patterns()

    def checker(self):
        self.input(self.patterns['checker'])

    def benchmark(self):
        for i in range(10000):
            self.input('l')

    def center_col(self, face):
        return self[face][1][1]

    def rotate_to_face_id(self, face):
        col = self.center_col(face)
        self.rotate_to_color(col)

    def rotate_to_color(self, col):
        for k, v in {'r': 'y-', 'l': 'y', 'u': 'x', 'd': 'x-', 'b': 'y2', 'f': ''}.items():
            if self.center_col(k) == col:
                self.input(v)
                break

    def rotate_face_to_face(self, face_org, face_dest):
        rotate = {
            'f': {'r': 'y-','l': 'y', 'u': 'x', 'd': 'x-','b': 'y2','f': ''},
            'b': {'r': 'y', 'l': 'y-','u': 'x-','d': 'x', 'b': '',  'f': 'y2'},
            'u': {'r': 'z', 'l': 'z-','u': '',  'd': 'z2','b': 'x', 'f': 'x-'},
            'd': {'r': 'z-','l': 'z', 'u': 'z2','d': '',  'b': 'x-','f': 'x'},
            'r': {'r': '',  'l': 'y2','u': 'z-','d': 'z', 'b': 'z-','f': 'z'},
            'l': {'r': 'y2','l': '',  'u': 'z', 'd': 'z-','b': 'z', 'f': 'z-'}
        }[face_dest][face_org]
        self.input(rotate)
        if rotate in ['z', 'z-', 'z2']:
            return {'z': -1, 'z-': 1, 'z2': 2}[rotate]
        return 0


    def get_face_by_col(self, col):
        for face in ['r', 'l', 'u', 'd', 'b', 'f']:
            if self.center_col(face) == col:
                return face

    def solve(self):
        self.front_col = 'w'
        self.cross()

    def cross(self):
        self.rotate_to_color(self.front_col)
        self.edge('r')
        self.edge('b')
        self.edge('o')
        self.edge('g')

    def edge(self, color):
        for face_id, face in self.items():
            self.rotate_to_face_id(face_id)
            brk = False
            edges = [(0, 1), (1, 2), (2, 1), (1, 0)]
            for it, (y, x) in enumerate(edges):
                bro = self.edge_brother(y, x)
                this = face[y][x]
                if (this == color and bro == 'w'):
                    front_face = self.get_face_by_col(self.front_col)
                    face_rot = self.rotate_face_to_face(front_face, 'u')
                    y, x = edges[(it + face_rot) % 4]
                    face_id = self.get_face_by_col(face[1][1])
                    if face_id in ['u', 'd']:
                        side = {(0, 1): 'u', (1, 2): 'r', (2, 1): 'd', (1, 0): 'l'}[(y,x)]
                        if face_id == 'u':
                            self.input({'u': ['b', 'l-', 'd', 'l'], 'd': ['f', 'r-', 'f-', 'd-'], 
                                        'r': ['r', 'b-', 'd2', 'b'], 'l': ['l-', 'b', 'd2', 'b-']}[side])
                        else:
                            self.input({'u': '', 'd': 'd2', 'r': 'd-', 'l': 'd'}[side])
                            self.input(['f', 'l', 'd', 'l-', 'd-', 'f-', 'd'])
                        color_face = self.get_face_by_col(color)
                        first_turn = {'f': [''], 'r': ['d', 'y-'], 'b': ['d2', 'y2'], 'l': ['d-', 'y']}[color_face]
                        self.input(first_turn + ['f2'])
                    else:
                        if face_id == 'b':
                            y, x = edges[(it + 2) % 4]
                        self.input({'b': 'y2', 'r': 'y-', 'f': '', 'l': 'y'}[face_id])
                        side = {(0, 1): 'u', (1, 2): 'r', (2, 1): 'd', (1, 0): 'l'}[(y,x)]
                        self.input({'u': ['f2'], 'd': [''], 
                                    'r': ['f', 'd', 'f-' ,'d-'], 'l': ['f-', 'd-', 'f', 'd']}[side])
                        color_face = self.get_face_by_col(color)
                        first_turn = {'f': [''], 'r': ['d', 'y-'], 'b': ['d2', 'y2'], 'l': ['d-', 'y']}[color_face]
                        self.input(first_turn + ['f2'])
                    brk = True
                    break
            self.rotate_to_color(self.front_col)
            if brk:
                break

    def edge_brother(self,y, x):
        direction = {(0, 1): 'u', (1, 0): 'l', (1, 2): 'r', (2, 1): 'd'}[(y,x)]
        newy, newx = {(0, 1): (2, 1), (1, 0): (1, 2), (1, 2): (1, 0), (2, 1): (0, 1)}[(y, x)]
        tile = self[direction][newy][newx]
        return tile
