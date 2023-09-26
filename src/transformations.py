from sequences import Sequence
from fasta import SeqFileManager


def duplicateManager(sequence, mode='original'):
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
                    id_dict[seq_id].id = '{}.{}'.format(seq_id, duplicate_count[seq_id])
                    seq.id = '{}.{}'.format(seq_id, duplicate_count[seq_id] + 1)
                    id_dict[seq.id] = seq
                    duplicate_count[seq_id] += 1
                else:
                    # Second or greater duplicate
                    duplicate_count[seq_id] += 1
                    seq.id = '{}.{}'.format(seq_id, duplicate_count[seq_id])
                    id_dict[seq.id] = seq
            elif mode == 'remove':
                if seq_id not in id_dict:
                    id_dict[seq_id] = seq
            else:
                return sequence
        else:
            id_dict[seq_id] = seq
    new_seq_list = list(id_dict.values())
    return new_seq_list

def reverseComplementSeq(sequence, style='original'):
    toret = []    
    if style == 'reverse':     
        for seq in sequence:              
            toret.append(Sequence(seq.id, seq.seq[::-1]))           
        return toret
    
    elif style == 'complement':
        complements = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
        for seq in sequence:
            toret.append(Sequence(seq.id, ''.join(complements[base] for base in seq.seq)))
        return toret 
        
    elif style == 'both':
        complements = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
        
        for seq in sequence:
            combined_seq = ''.join(complements[base] for base in seq.seq[::-1])
            toret.append(Sequence(seq.id, combined_seq))
        return toret
    
    elif style == 'original':
        toret = [i for i in sequence]
        return toret
    

if __name__ == '__main__':
    sequences = [
            Sequence('S1', 'TGAC'), Sequence('S1', 'GTCA'),
            Sequence('S2', 'CCCT'), Sequence('S3', 'AGGG'), 
            Sequence('S4', 'TCCC'), Sequence('S4', 'GGGA')
        ]

    load = SeqFileManager.loadFasta('test_3.fasta')

    d = duplicateManager(load, mode='rename')
    print(d)
    
    rc = reverseComplementSeq(d, 'both')
    print(rc)