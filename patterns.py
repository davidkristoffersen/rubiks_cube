class Patterns(dict):
    def __init__(self, extra = {}):
        if not isinstance(extra, dict):
            raise TypeError

        patterns = {
                'checker':      ['l2','r2','f2','b2','d2','u2'],
                'm_dot':        ['m', 'e-', 'm-', 'e'],
                'm_dot_back':   ['e-', 'm', 'e', 'm-']
            }
        patterns = {k: v for k, v in list(patterns.items()) + list(extra.items())}
        super().__init__(patterns)
