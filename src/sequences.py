# pylint: disable=duplicate-code
"""This module contains the Sequence class."""
## Definition of the Sequence class
class Sequence:
    """This class represents a sequence."""
    def __init__(self, seq_id, seq):
        self.id = seq_id
        self.seq = seq

    def __repr__(self):
        return f'{self.id}: {self.seq}'

    def __str__(self):
        return f'{self.id}: {self.seq}\n'
