# pylint: disable=duplicate-code
"""This module contains the classes that implement the transformations 
that can be applied to a list of sequences."""
from abc import ABC, abstractmethod
from sequences import Sequence


class AbstractTransformer(ABC):
    """Abstract class for sequence transformers."""
    @abstractmethod
    def transform(self, sequence):
        """Returns a list of Sequence objects with the transformation applied."""


class DuplicatedIdentifiersRemover(AbstractTransformer):
    """Removes duplicated identifiers from a list of Sequence objects."""
    def transform(self, sequence):
        new_seq_list = []
        id_dict = {}
        for seq in sequence:
            seq_id = seq.id
            if seq_id not in id_dict:
                id_dict[seq_id] = seq
        new_seq_list = list(id_dict.values())
        return new_seq_list


class DuplicatedIdentifiersRenamer(AbstractTransformer):
    """Renames duplicated identifiers from a list of Sequence objects."""
    def transform(self, sequence):
        new_seq_list = []
        id_dict = {}
        duplicate_count = {}
        for seq in sequence:
            seq_id = seq.id
            if seq_id in id_dict:
                if seq_id not in duplicate_count:
                    # First duplicate
                    duplicate_count[seq_id] = 1
                    id_dict[seq_id].id = f'{seq_id}.{duplicate_count[seq_id]}'
                    seq.id = f'{seq_id}.{duplicate_count[seq_id] + 1}'
                    id_dict[seq.id] = seq
                    duplicate_count[seq_id] += 1
                else:
                    # Second or grater duplicate
                    duplicate_count[seq_id] += 1
                    seq.id = f'{seq_id}.{duplicate_count[seq_id]}'
                    id_dict[seq.id] = seq
            else:
                id_dict[seq_id] = seq
        new_seq_list = list(id_dict.values())
        return new_seq_list


class ReverseComplement(AbstractTransformer):
    """Returns a list of Sequence objects with the reverse complement of the sequences."""
    def __init__(self, style):
        self.style = style

    def transform(self, sequence):
        toret = []
        if self.style == 'reverse':
            for seq in sequence:
                toret.append(Sequence(seq.id, seq.seq[::-1]))

        elif self.style == 'complement':
            complements = {
                            'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                            'a': 't', 'c': 'g', 'g': 'c', 't': 'a'
                            }
            for seq in sequence:
                toret.append(Sequence(seq.id, ''.join(complements[base] for base in seq.seq)))

        elif self.style == 'both':
            complements = {
                            'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                            'a': 't', 'c': 'g', 'g': 'c', 't': 'a'
                            }
            for seq in sequence:
                combined_seq = ''.join(complements[base] for base in seq.seq[::-1])
                toret.append(Sequence(seq.id, combined_seq))

        return toret


class SequenceListTransformer:
    """Class that applies a list of transformations to a list of sequences."""
    def __init__(self, sequence, transformation):
        self.sequence = sequence
        self.transformation = transformation

    def apply_transformations(self):
        """Returns a list of Sequence objects with the transformations applied."""
        transformed_list = self.sequence
        for transformation in self.transformation:
            transformed_list = transformation.transform(transformed_list)
        return transformed_list

if __name__ == '__main__':
    sequences = [
            Sequence('S1', 'TGAC'), Sequence('S1', 'GTCA'),
            Sequence('S2', 'CCCT'), Sequence('S3', 'AGGG'),
            Sequence('S4', 'TCCC'), Sequence('S4', 'GGGA')
        ]

    # Creating transformations
    transformations = [

        DuplicatedIdentifiersRenamer(),
        ReverseComplement(style='both')
    ]

    transformer = SequenceListTransformer(sequences, transformations)
    transformed = transformer.apply_transformations()
    print(transformed)
