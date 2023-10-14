# pylint: disable=duplicate-code
"""This module contains the class SeqFileManager, which allows us to format sequences 
and load and write fasta files."""
from enum import Enum
import sys
from sequences import Sequence

## We use class Enum for case=original/upper/lower
class Case(Enum):
    """Case enumerator"""
    ORIGINAL = 0
    UPPER = 1
    LOWER = 2

## We define the class that allows us to format sequences and load adn write fasta files.
class SeqFileManager:
    """This class allows us to format sequences and load and write fasta files."""
    def __init__(self, case=0, max_length=0):
        self.case = case
        self.max_length = max_length

    ## This function formats a sequence based by their length and case
    def format_sequence(self, sequence, case=Case.ORIGINAL, max_length=None):
        """Returns a string with the sequence formatted according to the parameters."""
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
            return f'>{sequence.seq_id}\n{seq}\n'

        seq_lines = [seq[i:i + max_length] for i in range(0, len(seq), max_length)]
        seq_formatted = '\n'.join(seq_lines)

        return f'>{sequence.seq_id}\n{seq_formatted}\n'

    ## This function loads the data from an existing file
    def load_fasta(self, file_name):
        """Returns a list of Sequence objects from the fasta file."""
        sequences = [] # List of Sequence objects
        with open(file_name, encoding="utf-8") as f:
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
        """Writes the sequences to the file_path."""
        with open(file_path, 'w', encoding="utf-8") as f:
            for sequence in sequences:
                formatted_sequence = self.format_sequence(sequence)
                f.write(formatted_sequence)
                f.write('\n')

    ## Function to parse the value of the Case enumerator
    @staticmethod
    def parse_case(case):
        """Returns a Case object from the string case."""
        if isinstance(case, str):
            case = getattr(Case, case.upper())
        return case


#### FUNCTIONS ####
# Error function in case max_length is less than 0.
def error_length(max_length):
    """Returns an error if max_length is less than 0."""
    if float(max_length).is_integer():
        if int(max_length) < 0:
            raise ValueError('max_length must be >= 0.')

    elif float(max_length).is_integer() is False:
        raise ValueError('max_length must be an integer.')

def error_generic(args, module):
    """Returns an error if the required parameters are missing."""
    if args['input'] == 'error' or args['output'] == 'error':
        print('[ERROR] Required parameters are missing.')
        print(f'Use: python {module} --input=/path/to/input.fasta--output=/path/to/output.fasta')
        sys.exit(1)

def error_mode(args, module):
    """Returns an error if the mode is not correct."""
    if module == 'disambiguate.py' and args['mode'] == 'error':
        print('[ERROR] Required parameters are missing.')
        print(f'Use: python {module} --input=/path/to/input.fasta ' +
                                    '--output=/path/to/output.fasta ' +
                                    '--mode=original/rename/remove')
        sys.exit(1)

    elif module == 'reverse_complement.py' and 'mode' not in args:
        print('[ERROR] Required parameters are missing.')
        print(f'Use: python {module} --input=/path/to/input.fasta ' +
                                    '--output=/path/to/output.fasta ' +
                                    '--mode=original/reverse/complement/both')
        sys.exit(1)


def error_path(args, module):
    """Returns an error if the path is not correct."""
    if module == 'fasta_summary.py':
        if 'extra-plots-dir' in args and args['extra-plots-dir'] == 'error':
            print('[ERROR] You have not indicated a correct route.')
            print(f'Use: python {module} --input=/path/to/input.fasta ' +
                                        '--output=/path/to/output.fasta ' +
                                        '––extra–plots-dir=/path/to/dir')
            sys.exit(1)
