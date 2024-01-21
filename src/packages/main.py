'''Main module for the FASTA file processing tool'''
import argparse
import os

from packages.utils.seq_file_manager import SeqFileManager
from packages.plots.plot_generator import PlotGenerator
from packages.sequences.sequences import Sequence
from packages.transformers.duplicated_transformer import DuplicatedTransformer
from packages.transformers.reverse_complement import ReverseComplement
from packages.stats.sequence_stats import SequenceStats

def main():
    '''Main function'''
    parser = argparse.ArgumentParser(description='FASTA file processing tool')
    parser.add_argument('--dremove', action='store_true', help='Remove duplicates')
    parser.add_argument('--drename', action='store_true', help='Rename duplicates')
    parser.add_argument('--reverse', action='store_true', help='Reverse sequences')
    parser.add_argument('--complement', action='store_true', help='Complement sequences')
    parser.add_argument('--rc', action='store_true', help='Reverse complement sequences')
    parser.add_argument('--stats', help='Compute stats', action='store_true')
    parser.add_argument('--casefile', help='Case transformation (original, upper, lower)')
    parser.add_argument('--plots', help='Generate plots', action='store_true')
    args = parser.parse_args()


    # Get the FASTA files in the current directory
    current_directory = os.getcwd()
    fasta_files = [file for file in os.listdir(current_directory) if file.endswith('.fasta')]

    # Verify that there are FASTA files in the current directory
    if not any([args.casefile, args.dremove, args.drename, args.reverse, args.complement, args.rc, args.stats, args.plots]):
        print('No transformation specified')
        return

    if not fasta_files:
        print('No FASTA files found in the current directory')
        return
    
    stats_directory = os.path.join(current_directory, 'result_stats')

    for filename in fasta_files:
        seq_file_manager = SeqFileManager(case=args.casefile, input_filename=filename)
        sequences = seq_file_manager.load_fasta(filename)

        # Apply case transformation if specified
        if args.casefile == 'upper':
            sequences = [Sequence(seq.id, seq.seq.upper(), seq.file_name) for seq in sequences]
        elif args.casefile == 'lower':
            sequences = [Sequence(seq.id, seq.seq.lower(), seq.file_name) for seq in sequences]

        if args.dremove:
            # Remove duplicates
            sequences = DuplicatedTransformer(style='remove').transform(sequences)
        elif args.drename:
            # Rename duplicates
            sequences = DuplicatedTransformer(style='rename').transform(sequences)

        if args.reverse:
            # Reverse sequences
            sequences = ReverseComplement(style='reverse').transform(sequences)

        elif args.complement:
            # Complement sequences
            sequences = ReverseComplement(style='complement').transform(sequences)

        elif args.rc:
            # Reverse complement sequences
            sequences = ReverseComplement(style='both').transform(sequences)

        if args.plots:
            plot_generator = PlotGenerator(sequences, filename, 'result_plots')
            plot_generator.generate_plots()

        if args.stats:
            sequence_stats = SequenceStats()
            sequence_stats.generate_stats(sequences, stats_directory, filename)

        # Process the sequences if any transformation was specified
        if any([args.casefile, args.dremove, args.drename, args.reverse, args.complement, args.rc]):
            output_directory = os.path.join(current_directory, 'result_formatted')
            seq_file_manager.write_fasta(sequences, output_directory)

if __name__ == '__main__':
    main()
