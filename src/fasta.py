from sequences import Sequence
from enum import Enum
import sys

## We use class Enum for case=original/upper/lower
class Case(Enum):
    ORIGINAL = 0
    UPPER = 1
    LOWER = 2  

## We define the class that allows us to format sequences and load adn write fasta files.
class SeqFileManager:
    def __init__(self, case=0, maxLength=0):
        self.case = case
        self.maxLength = maxLength

    ## This function formats a sequence based by their length and case
    def formatSequence(self, sequence, case=Case.ORIGINAL, maxLength=None):           
        seq = sequence.seq

        if case == Case.ORIGINAL:
            case = self.case
        if case == Case.UPPER:
            seq = seq.upper() # Convert the sequence to uppercase
        elif case == Case.LOWER:
            seq = seq.lower() # Convert the sequence to lowercase
        
        if maxLength is None:
            maxLength = self.maxLength        
        if maxLength == 0:
            return '>{}\n{}\n'.format(sequence.id, seq)

        seq_lines = [seq[i:i + maxLength] for i in range(0, len(seq), maxLength)]
        seq_formatted = '\n'.join(seq_lines)

        return '>{}\n{}\n'.format(sequence.id, seq_formatted)

    ## This function loads the data from an existing file
    def loadFasta(fileName):
        sequences = [] # List of Sequence objects
        with open(fileName) as f:
            inSequence = False # This variable determines if we are in a sequence or not
            seqLines = [] # New list that will have the lines of the sequence
            id = None # sequence ID
            for line in f:
                if line.startswith('>'):
                    if inSequence:
                        seq = ''.join(seqLines) # joins the sequence lines
                        sequences.append(Sequence(id, seq))  
                        seqLines = [] # Empties the list of lines
                    id = line.strip()[1:] # Gets the ID
                    inSequence = True
                else:
                    seqLines.append(line.strip()) # Add the line to the line list
            if inSequence:
                seq = ''.join(seqLines) # Join the lines of the last sequence
                sequences.append(Sequence(id, seq)) # Add to the sequences list an object that will have an ID and a seq (sequence) 
        return sequences
    
    ## This function writes the data into a new file
    def writeFasta(self, sequences, filePath):
        with open(filePath, 'w') as f:
            for sequence in sequences:
                formatted_sequence = self.formatSequence(sequence)
                f.write(formatted_sequence)
                f.write('\n')

    ## Function to parse the value of the Case enumerator
    @staticmethod
    def parseCase(case):
        if isinstance(case, str):
            case = getattr(Case, case.upper())
        return case


#### FUNCTIONS ####
# Error function in case maxLength is less than 0.
def errorLength(maxLength):
    if float(maxLength).is_integer():
        if int(maxLength) < 0:            
            raise ValueError('maxLength must be >= 0.')
        
    elif float(maxLength).is_integer() == False:
        raise ValueError('maxLength must be an integer.')    

def errorGeneric(args, module):        
    if args['input'] == 'error' or args['output'] == 'error':
        print('[ERROR] Required parameters are missing.')
        print(f'Use: python {module} --input=/path/to/input.fasta --output=/path/to/output.fasta')
        sys.exit(1)

def errorMode(args, module):    
    if module == 'disambiguate.py' and args['mode'] == 'error':   
        print('[ERROR] Required parameters are missing.')
        print(f'Use: python {module} --input=/path/to/input.fasta --output=/path/to/output.fasta --mode=original/rename/remove')
        sys.exit(1)

    elif module == 'reverse_complement.py' and 'mode' not in args:
        print('[ERROR] Required parameters are missing.')
        print(f'Use: python {module} --input=/path/to/input.fasta --output=/path/to/output.fasta --mode=original/reverse/complement/both')
        sys.exit(1)


def errorPath(args, module):
    if module == 'fasta_summary.py':
        if 'extra-plots-dir' in args and args['extra-plots-dir'] == 'error':
            print('[ERROR] You have not indicated a correct route.')
            print(f'Use: python {module} --input=/path/to/input.fasta --output=/path/to/output.fasta ––extra–plots-dir=/path/to/dir')
            sys.exit(1)


    
