"""Module for generating plots from sequences."""
import os
import pandas as pd
import matplotlib.pyplot as plt

class PlotGenerator:
    '''Class for generating plots from sequences.'''
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
