# src/main.py
import argparse
import os

from packages.Utils.seq_file_manager import SeqFileManager
from packages.Plots.plot_generator import PlotGenerator
from packages.Sequences.sequences import Sequence
from packages.Transformers.duplicated_transformer import DuplicatedTransformer
from packages.Transformers.reverse_complement import ReverseComplement
from packages.Stats.sequence_stats import SequenceStats

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
    parser.add_argument('--maxlength', type=int, default=0, help='Maximum line length (0 for no limit)')
    parser.add_argument('--plots', help='Generate plots', action='store_true')
    args = parser.parse_args()

    # Verificar si se proporcionó al menos una opción de reformateado
    if not any([args.casefile, args.maxlength, args.dremove, args.drename, args.reverse, args.complement, args.rc]):
        print("No se especificó ningún tipo de reformateado. No se crearán carpetas de resultados.")

    # Obtener la lista de archivos .fasta en el directorio actual
    current_directory = os.getcwd()
    fasta_files = [file for file in os.listdir(current_directory) if file.endswith('.fasta')]

    # Verificar si hay archivos .fasta en el directorio
    if not fasta_files:
        print("No se encontraron archivos .fasta en el directorio actual.")
        return

    stats_directory = os.path.join(current_directory, 'stats')

    for filename in fasta_files:
        seq_file_manager = SeqFileManager(case=args.casefile, max_length=args.maxlength, input_filename=filename)
        sequences = seq_file_manager.load_fasta(filename)

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

        # Aplicar la longitud máxima a cada línea si se especifica args.maxlength
        sequences = [seq.max_length(args.maxlength) if args.maxlength else seq for seq in sequences]

        if args.plots:
            PlotGenerator.generate_plots(sequences, filename, 'plots')

        if args.stats:
            SequenceStats.generate_stats(sequences, stats_directory, filename)

        # Ahora escribimos las secuencias procesadas solo si se especificó algún tipo de reformateado
        if any([args.casefile, args.maxlength, args.dremove, args.drename, args.reverse, args.complement, args.rc]):
            output_directory = os.path.join(current_directory, 'results')
            seq_file_manager.write_fasta(sequences, output_directory)

if __name__ == '__main__':
    main()
