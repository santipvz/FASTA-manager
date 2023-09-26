from sequences import Sequence
import csv

class SequenceStats:
    def getSeqStats(sequence):
        # Calculates statistics for an individual sequence
        length = len(sequence.seq)
        counts = {'A': 0, 'C': 0, 'T': 0, 'G': 0, '-': 0}
        
        for base in sequence.seq:
            if base in counts:
                counts[base] += 1
        
        # Return statistics in a list
        stats = [sequence.id, length] + [counts[base] for base in 'ACTG-']
        return stats

    def getSeqStatsMatrix(sequences):
        # Computes statistics matrix for a list of sequences
        header = ['id', 'len', 'A', 'C', 'T', 'G', '-']
        matrix = [header]
        
        for sequence in sequences:
            stats = SequenceStats.getSeqStats(sequence)
            matrix.append(stats)
        
        # Returns the statistics array
        return matrix
    
    def statsMatrixToCsv(matrix, filepath):
        # Write the statistics array to a CSV file
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(matrix)

if __name__ == '__main__':
    # Example of use with test sequences
    sequences = [
        Sequence('S1', 'AAAACCCTTG'),
        Sequence('S2', 'TATTGGGC-')
    ]
    
    # Get the statistics array
    stats_matrix = SequenceStats.getSeqStatsMatrix(sequences)
    
    # Write statistics array to CSV file
    SequenceStats.statsMatrixToCsv(stats_matrix, 'fichero.csv')
    
    # Print the statistics matrix
    for row in stats_matrix:
        print(row)
