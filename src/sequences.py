
## Definition of the Sequence class
class Sequence:
    def __init__(self, id, seq):
        self.id = id
        self.seq = seq

    def __repr__(self):
        return '{}: {}'.format(self.id, self.seq)

    def __str__(self):
        return '{}: {}\n'.format(self.id, self.seq)