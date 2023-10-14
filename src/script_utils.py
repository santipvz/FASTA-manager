"""This module contains the functions that are used by the scripts 
to apply the transformations to the sequences."""
import sys
from fasta import SeqFileManager, error_length, error_mode
from argsparser import parse_args


args = parse_args(sys.argv[1:])

def arguments():
    """Returns the input and output files from the arguments passed to the script."""
    toret = []
    toret.append(args['input'])
    toret.append(args['output'])

    return toret

error_mode(args, sys.argv[0])
script_args = arguments()

caseFile = args.get('case', 'original')
maxLengthFile = args.get('maxLength', '0')

if maxLengthFile.isdigit():
    maxLengthFile = int(maxLengthFile)
else:
    error_length(maxLengthFile)


def apply_transformation(input_file, output_file, transformation):
    """Applies the transformation to the sequences in the input file and 
    writes the result to the output file."""
    # Load sequence list from input file
    load = SeqFileManager().load_fasta(input_file)
    # Write sequence list to output file
    SeqFileManager(SeqFileManager.parse_case(caseFile),
                    maxLengthFile).write_fasta(transformation(load), output_file)
