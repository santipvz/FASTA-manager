import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from argsparser import parseArgs
from fasta import SeqFileManager, errorGeneric, errorPath
from sequence_stats import SequenceStats


def generatePlots(statsDataFrame, inputFilePath, extraPlotsDir):
    # Get the input file name without the extension
    inputFileName = os.path.splitext(os.path.basename(inputFilePath))[0]

    # Sequence length histogram
    sequence_lengths = statsDataFrame['len']
    plt.hist(sequence_lengths, bins=10, color='#DDA0DD')
    plt.xlabel('Sequence length')
    plt.ylabel('Frequency')
    plt.title('Histogram of sequence length distribution')
    histogram_filename = inputFileName + '_histogram.png'
    histogram_filepath = os.path.join(extraPlotsDir, histogram_filename)
    plt.savefig(histogram_filepath)
    plt.close()

    # Box plot
    base_counts = ['A', 'C', 'T', 'G']
    base_percentages = statsDataFrame[base_counts].divide(statsDataFrame['len'], axis=0)
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
    boxplot_filename = inputFileName + '_boxplot.png'
    boxplot_filepath = os.path.join(extraPlotsDir, boxplot_filename)
    plt.savefig(boxplot_filepath)
    plt.close()


args = parseArgs(sys.argv[1:])
errorGeneric(args, sys.argv[0])
extraPlotsDir = args.get('extra-plots-dir', None)
errorPath(args, sys.argv[0])


inputPath = args['input']
outputPath = args['output']

# Create the directory for the csv and plots if they do not exist
if not os.path.exists(outputPath):
    os.makedirs(outputPath) 
if not os.path.exists(extraPlotsDir):
    os.makedirs(extraPlotsDir)


if os.path.isfile(inputPath):  # If the input path is a file
    # Process a single file
    load = SeqFileManager.loadFasta(inputPath)
    stats_matrix = SequenceStats.getSeqStatsMatrix(load)
    SequenceStats.statsMatrixToCsv(stats_matrix, outputPath)
    statsDataFrame = pd.DataFrame(stats_matrix[1:], columns=stats_matrix[0])
    if extraPlotsDir is not None:
        generatePlots(statsDataFrame, inputPath, extraPlotsDir)

elif os.path.isdir(inputPath):  # If the input path is a directory
    # Process files in directory
    for filename in os.listdir(inputPath):
        if filename.endswith('.fasta'):
            inputFilePath = os.path.join(inputPath, filename)
            load = SeqFileManager.loadFasta(inputFilePath)
            stats_matrix = SequenceStats.getSeqStatsMatrix(load)
            outputFileName = os.path.splitext(filename)[0] + '.csv'
            outputFilePath = os.path.join(outputPath, outputFileName)
            SequenceStats.statsMatrixToCsv(stats_matrix, outputFilePath)
            statsDataFrame = pd.DataFrame(stats_matrix[1:], columns=stats_matrix[0])
            if extraPlotsDir is not None:
                generatePlots(statsDataFrame, inputFilePath, extraPlotsDir)