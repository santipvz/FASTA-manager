# pylint: disable=duplicate-code
"""This module contains functions for transforming sequences."""
from sequences import Sequence
from fasta import SeqFileManager


def duplicate_manager(sequence, mode='original'):
    """Returns a list of Sequence objects without duplicates."""
    new_seq_list = []
    id_dict = {}
    duplicate_count = {}
    for seq in sequence:
        seq_id = seq.id
        if seq_id in id_dict:
            if mode == 'rename':
                if seq_id not in duplicate_count:
                    # First duplicate
                    duplicate_count[seq_id] = 1
                    id_dict[seq_id].id = f'{seq_id}.{duplicate_count[seq_id]}'
                    seq.id = f'{seq_id}.{duplicate_count[seq_id] + 1}'
                    id_dict[seq.id] = seq
                    duplicate_count[seq_id] += 1
                else:
                    # Second or greater duplicate
                    duplicate_count[seq_id] += 1
                    seq.id = f'{seq_id}.{duplicate_count[seq_id]}'
                    id_dict[seq.id] = seq
            elif mode == 'remove':
                if seq_id not in id_dict:
                    id_dict[seq_id] = seq
            else:
                return sequence
        else:
            id_dict[seq_id] = seq
    new_seq_list = list(id_dict.values())
    return new_seq_list if new_seq_list else None

def reverse_complement(sequence, style='original'):
    """Returns a list of Sequence objects with the reverse complement of the sequences."""
    toret = []
    if style == 'reverse':
        for seq in sequence:
            toret.append(Sequence(seq.id, seq.seq[::-1]))
        return toret

    elif style == 'complement':
        complements = {
                        'A': 'T', 'C': 'G', 'G': 'C','T': 'A',
                        'a': 't', 'c': 'g', 'g': 'c', 't': 'a'
                        }

        for seq in sequence:
            toret.append(Sequence(seq.id, ''.join(complements[base] for base in seq.seq)))
        return toret

    elif style == 'both':
        complements = {
                        'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                        'a': 't', 'c': 'g', 'g': 'c', 't': 'a'
                        }

        for seq in sequence:
            combined_seq = ''.join(complements[base] for base in seq.seq[::-1])
            toret.append(Sequence(seq.id, combined_seq))
        return toret

    else:
        toret = list(sequence)
        return toret if toret else None


if __name__ == '__main__':
    sequences = [
            Sequence('S1', 'TGAC'), Sequence('S1', 'GTCA'),
            Sequence('S2', 'CCCT'), Sequence('S3', 'AGGG'),
            Sequence('S4', 'TCCC'), Sequence('S4', 'GGGA')
        ]

    load = SeqFileManager().load_fasta('assets/test_3.fasta')

    d = duplicate_manager(load, mode='rename')
    print(d)

    rc = reverse_complement(d, 'both')
    print(rc)