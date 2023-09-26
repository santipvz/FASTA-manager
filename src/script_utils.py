import sys
from fasta import SeqFileManager, errorLength, errorMode
from src.argsparser import parseArgs


args = parseArgs(sys.argv[1:])
# We save ourselves from duplicating the arguments in each file with this function
def arguments():
    toret = []
    toret.append(args['input'])
    toret.append(args['output'])

    return toret

errorMode(args, sys.argv[0])
script_args = arguments()

caseFile = args.get('case', 'original')
maxLengthFile = args.get('maxLength', '0')

if maxLengthFile.isdigit():
    maxLengthFile = int(maxLengthFile)
else:
    errorLength(maxLengthFile) 
    

def apply_transformation(inputFile, outputFile, transformation):
    # Load sequence list from input file
    load = SeqFileManager.loadFasta(inputFile)   
    # Write sequence list to output file
    SeqFileManager(SeqFileManager.parseCase(caseFile), maxLengthFile).writeFasta(transformation(load), outputFile)

