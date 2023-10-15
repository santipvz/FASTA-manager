'''This module contains the class SeqFileManager, which allows us to format sequences 
and load and write fasta files.'''
import argparse
from enum import Enum
import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import DuplicatedIdentifiersRenamer,DuplicatedIdentifiersRemover,ReverseComplement
from sequence_stats import SequenceStats
from sequences import Sequence

## We use class Enum for case=original/upper/lower
class Case(Enum):
    '''Case enumerator'''
    ORIGINAL = 0
    UPPER = 1
    LOWER = 2

## We define the class that allows us to format sequences and load adn write fasta files.
class SeqFileManager:
    '''This class allows us to format sequences and load and write fasta files.'''
    def __init__(self, case=0, max_length=0):
        self.case = case
        self.max_length = max_length

    ## This function formats a sequence based by their length and case
    def format_sequence(self, sequence, case=Case.ORIGINAL, max_length=None):
        '''Returns a string with the sequence formatted according to the parameters.'''
        seq = sequence.seq

        if case == Case.ORIGINAL:
            case = self.case
        if case == Case.UPPER:
            seq = seq.upper() # Convert the sequence to uppercase
        elif case == Case.LOWER:
            seq = seq.lower() # Convert the sequence to lowercase

        if max_length is None:
            max_length = self.max_length
        if max_length == 0:
            return f'>{sequence.id}\n{seq}\n'

        seq_lines = [seq[i:i + max_length] for i in range(0, len(seq), max_length)]
        seq_formatted = '\n'.join(seq_lines)

        return f'>{sequence.id}\n{seq_formatted}\n'

    ## This function loads the data from an existing file
    def load_fasta(self, file_name):
        '''Returns a list of Sequence objects from the fasta file.'''
        sequences = [] # List of Sequence objects
        with open(file_name, encoding='utf-8') as f:
            in_sequence = False # This variable determines if we are in a sequence or not
            seq_lines = [] # New list that will have the lines of the sequence
            seq_id = None # sequence seq_id
            for line in f:
                if line.startswith('>'):
                    if in_sequence:
                        seq = ''.join(seq_lines) # joins the sequence lines
                        sequences.append(Sequence(seq_id, seq))
                        seq_lines = [] # Empties the list of lines
                    seq_id = line.strip()[1:] # Gets the seq_id
                    in_sequence = True
                else:
                    seq_lines.append(line.strip()) # Add the line to the line list
            if in_sequence:
                seq = ''.join(seq_lines) # Join the lines of the last sequence
                sequences.append(Sequence(seq_id, seq))
                # Add to the sequences list an object that will have an seq_id and a seq (sequence)
        return sequences

    ## This function writes the data into a new file
    def write_fasta(self, sequences, file_path):
        '''Writes the sequences to the file_path.'''
        with open(file_path, 'w', encoding='utf-8') as f:
            for sequence in sequences:
                formatted_sequence = self.format_sequence(sequence)
                f.write(formatted_sequence)
                f.write('\n')

    ## Function to parse the value of the Case enumerator
    @staticmethod
    def parse_case(case):
        '''Returns a Case object from the string case.'''
        if isinstance(case, str):
            case = getattr(Case, case.upper())
        return case

def generate_plots(sequences, input_path, plots_dir):
    '''Generates plots from the sequences.'''
    # Create lists to store data for DataFrame
    seq_ids = [seq.id for seq in sequences]
    seq_lengths = [len(seq.seq) for seq in sequences]

    # Calculate the count of each base in each sequence
    base_counts = {'A': [], 'C': [], 'T': [], 'G': []}
    for seq in sequences:
        for base, count_list in base_counts.items():
            count_list.append(seq.seq.count(base))

    # Create a DataFrame from the collected data
    data = {
        'seq_id': seq_ids,
        'len': seq_lengths,
        'A': base_counts['A'],
        'C': base_counts['C'],
        'T': base_counts['T'],
        'G': base_counts['G']
    }
    df = pd.DataFrame(data)

    # Get the input file name without the extension
    input_file_name = os.path.splitext(os.path.basename(input_path))[0]

    # Sequence length histogram
    sequence_lengths = df['len']
    plt.hist(sequence_lengths, bins=10, color='#DDA0DD')
    plt.xlabel('Sequence length')
    plt.ylabel('Frequency')
    plt.title('Histogram of sequence length distribution')
    histogram_filename = input_file_name + '_histogram.png'
    histogram_filepath = os.path.join(plots_dir, histogram_filename)

    # Create the directory if it doesn't exist
    os.makedirs(plots_dir, exist_ok=True)

    plt.savefig(histogram_filepath)
    plt.close()

    # Calculate the base percentages
    base_counts = ['A', 'C', 'T', 'G']
    total_lengths = df['len']
    for base in base_counts:
        df[base] = df[base] / total_lengths

    # Box plot
    box_colors = ['#FFC0CB', '#ADD8E6', '#90EE90', '#FFFF66']
    plt.boxplot(df[base_counts].values, labels=base_counts, patch_artist=True)

    # Personalize box colors
    for patch, color in zip(plt.boxplot(df[base_counts].values, patch_artist=True)['boxes'],
                                        box_colors):
        patch.set_facecolor(color)

    plt.xlabel('Bases')
    plt.ylabel('Percentage')
    plt.title('Relative percentage of bases in the total length of sequences')
    plt.grid(True)
    boxplot_filename = input_file_name + '_boxplot.png'
    boxplot_filepath = os.path.join(plots_dir, boxplot_filename)
    plt.savefig(boxplot_filepath)
    plt.close()

def main():
    '''Main function'''
    parser = argparse.ArgumentParser(description='FASTA file processing tool')
    parser.add_argument('--input',
                        required=True,
                        help='Input FASTA file or directory path')

    parser.add_argument('--output',
                        required=True,
                        help='Output directory path')

    parser.add_argument('--dremove',
                        action='store_true',
                        help='Remove duplicates')

    parser.add_argument('--drename',
                        action='store_true',
                        help='Rename duplicates')

    parser.add_argument('--reverse',
                        action='store_true',
                        help='Reverse sequences')

    parser.add_argument('--complement',
                        action='store_true',
                        help='Complement sequences')

    parser.add_argument('--rc',
                        action='store_true',
                        help='Reverse complement sequences')

    parser.add_argument('--stats',
                        action='store_true',
                        help='Compute statistics')

    parser.add_argument('--casefile',
                        default='original',
                        help='Case transformation (original, upper, lower)')

    parser.add_argument('--maxlength',
                        type=int,
                        default=0,
                        help='Maximum line length (0 for no limit)')

    parser.add_argument('--extra-plots-dir',
                        help='Directory for extra plots')

    args = parser.parse_args()

    if not (args.dremove or args.drename or args.reverse
            or args.complement or args.rc or args.stats or args.extra_plots_dir):
        print('Please specify an action'+
            '(--dremove, --drename, --reverse, --complement, --rc, --stats or --extra-plots-dir).')
        return

    sequence_manager = SeqFileManager(SeqFileManager.parse_case(args.casefile), args.maxlength)

    # Check if --input is a directory
    if os.path.isdir(args.input):  # If the input path is a directory
        # Process files in the directory
        for filename in os.listdir(args.input):
            if filename.endswith('.fasta'):
                input_file_path = os.path.join(args.input, filename)
                load = sequence_manager.load_fasta(input_file_path)
                output_file_name = os.path.splitext(filename)[0] + '.csv'

                # Combine the output directory and filename
                output_file_path = os.path.join(args.output, output_file_name)

                # Create the output directory if it doesn't exist
                os.makedirs(args.output, exist_ok=True)

                sequences = process_sequences(load, args)
                write_output(sequence_manager, sequences, output_file_path)

                if args.extra_plots_dir is not None:
                    generate_plots(sequences, input_file_path, args.extra_plots_dir)

                if args.stats:
                    # Compute statistics and save to a CSV file
                    stats_matrix = SequenceStats().get_seq_stats_matrix(sequences)
                    stats_filename = os.path.splitext(filename)[0] + '_stats.csv'
                    stats_filepath = os.path.join(args.output, stats_filename)
                    SequenceStats().stats_to_csv(stats_matrix, stats_filepath)

    elif os.path.isfile(args.input):  # If the input path is a file
        # Process a single file
        load = sequence_manager.load_fasta(args.input)
        sequences = process_sequences(load, args)

        if args.extra_plots_dir is not None:
            output_file_path = os.path.join(args.output, 'output.csv')
            write_output(sequence_manager, sequences, output_file_path)
            generate_plots(sequences, args.input, args.extra_plots_dir)

        if args.stats:
            # Compute statistics and save to a CSV file
            stats_matrix = SequenceStats().get_seq_stats_matrix(sequences)
            stats_filepath = os.path.join(args.output, args.input + '_stats.csv')
            SequenceStats().stats_to_csv(stats_matrix, stats_filepath)

def process_sequences(sequences, args):
    '''Process the sequences according to the arguments.'''
    if args.dremove:
        # Remove duplicates
        sequences = DuplicatedIdentifiersRemover().transform(sequences)
    if args.drename:
        # Rename duplicates
        sequences = DuplicatedIdentifiersRenamer().transform(sequences)

    if args.reverse:
        # Reverse sequences
        sequences = ReverseComplement(style='reverse').transform(sequences)

    if args.complement:
        # Complement sequences
        sequences = ReverseComplement(style='complement').transform(sequences)

    if args.rc:
        # Reverse complement sequences
        sequences = ReverseComplement(style='both').transform(sequences)

    SeqFileManager(SeqFileManager.parse_case(args.casefile), args.maxlength).write_fasta(sequences, args.output)
    return sequences

def write_output(sequence_manager, sequences, output_file_path):
    '''Writes the sequences to the output file.'''
    sequence_manager.write_fasta(sequences, output_file_path)

if __name__ == '__main__':
    main()