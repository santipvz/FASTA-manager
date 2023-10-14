# pylint: disable=duplicate-code
""" This script takes a fasta file or a directory containing fasta files and
    generates a csv file with the statistics of the sequences in the fasta file
    or in the fasta files in the directory. It also generates a histogram and a
    box plot of the sequence length distribution and the relative percentage of
    bases in the total length of sequences, respectively, if the user specifies
    a directory containing fasta files."""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from argsparser import parse_args
from fasta import SeqFileManager, error_generic, error_path
from sequence_stats import SequenceStats


def generate_plots(data_frame, input_path, plots_dir):
    """Generates a histogram and a box plot of the sequence length distribution
    and the relative percentage of bases in the total length of sequences,
    respectively, and saves them in the plots directory."""

    # Get the input file name without the extension
    input_file_name = os.path.splitext(os.path.basename(input_path))[0]

    # Sequence length histogram
    sequence_lengths = data_frame['len']
    plt.hist(sequence_lengths, bins=10, color='#DDA0DD')
    plt.xlabel('Sequence length')
    plt.ylabel('Frequency')
    plt.title('Histogram of sequence length distribution')
    histogram_filename = input_file_name + '_histogram.png'
    histogram_filepath = os.path.join(plots_dir, histogram_filename)
    plt.savefig(histogram_filepath)
    plt.close()

    # Box plot
    base_counts = ['A', 'C', 'T', 'G']
    base_percentages = data_frame[base_counts].divide(data_frame['len'], axis=0)
    # Box colors
    box_colors = ['#FFC0CB', '#ADD8E6', '#90EE90', '#FFFF66']
    # Create the box plot
    boxplot = plt.boxplot(base_percentages.values, labels=base_counts, patch_artist=True)
    # Personalize box colors
    for patch, color in zip(boxplot['boxes'], box_colors):
        patch.set_facecolor(color)

    plt.xlabel('Bases')
    plt.ylabel('Percentage')
    plt.title('Relative percentage of bases in the total length of sequences')
    plt.grid(True)
    boxplot_filename = input_file_name + '_boxplot.png'
    boxplot_filepath = os.path.join(plots_dir, boxplot_filename)
    plt.savefig(boxplot_filepath)
    plt.close()


args = parse_args(sys.argv[1:])
error_generic(args, sys.argv[0])
extra_plots_dir = args.get('extra-plots-dir', None)
error_path(args, sys.argv[0])


inputPath = args['input']
outputPath = args['output']

# Create the directory for the csv and plots if they do not exist
if not os.path.exists(outputPath):
    os.makedirs(outputPath)
if not os.path.exists(extra_plots_dir):
    os.makedirs(extra_plots_dir)


if os.path.isfile(inputPath):  # If the input path is a file
    # Process a single file
    load = SeqFileManager().load_fasta(inputPath)
    stats_matrix = SequenceStats().get_seq_stats_matrix(load)
    SequenceStats().stats_to_csv(stats_matrix, outputPath)
    stats_data_frame = pd.DataFrame(stats_matrix[1:], columns=stats_matrix[0])
    if extra_plots_dir is not None:
        generate_plots(stats_data_frame, inputPath, extra_plots_dir)

elif os.path.isdir(inputPath):  # If the input path is a directory
    # Process files in directory
    for filename in os.listdir(inputPath):
        if filename.endswith('.fasta'):
            input_file_path = os.path.join(inputPath, filename)
            load = SeqFileManager().load_fasta(input_file_path)
            stats_matrix = SequenceStats().get_seq_stats_matrix(load)
            outputFileName = os.path.splitext(filename)[0] + '.csv'
            outputFilePath = os.path.join(outputPath, outputFileName)
            SequenceStats().stats_to_csv(stats_matrix, outputFilePath)
            stats_data_frame = pd.DataFrame(stats_matrix[1:], columns=stats_matrix[0])
            if extra_plots_dir is not None:
                generate_plots(stats_data_frame, input_file_path, extra_plots_dir)
